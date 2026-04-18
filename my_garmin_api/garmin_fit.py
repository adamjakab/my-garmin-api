"""Garmin activity data aggregation helpers."""

import os
from collections.abc import Callable
from datetime import date, timedelta
from pathlib import Path
import sys
from typing import Any

from dotenv import load_dotenv
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

from .garmin_cache import get_cache_key, load_cached_data, save_cached_data


load_dotenv()


ActivityResourceFetcher = Callable[[Garmin, str], Any]

ACTIVITY_RESOURCE_FETCHERS: tuple[tuple[str, ActivityResourceFetcher], ...] = (
    # ("activity", lambda api, activity_id: api.get_activity(activity_id)),
    # ("details", lambda api, activity_id: api.get_activity_details(activity_id)),
    # ("splits", lambda api, activity_id: api.get_activity_splits(activity_id)),
    # (
    #     "typed_splits",
    #     lambda api, activity_id: api.get_activity_typed_splits(activity_id),
    # ),
    # (
    #     "split_summaries",
    #     lambda api, activity_id: api.get_activity_split_summaries(activity_id),
    # ),
    # ("weather", lambda api, activity_id: api.get_activity_weather(activity_id)),
    # (
    #     "hr_time_in_zones",
    #     lambda api, activity_id: api.get_activity_hr_in_timezones(activity_id),
    # ),
    # (
    #     "power_time_in_zones",
    #     lambda api, activity_id: api.get_activity_power_in_timezones(activity_id),
    # ),
    # (
    #     "exercise_sets",
    #     lambda api, activity_id: api.get_activity_exercise_sets(activity_id),
    # ),
    # ("gear", lambda api, activity_id: api.get_activity_gear(activity_id)),
)


def _safe_fetch_activity_resource(
    api: Garmin,
    activity_id: str,
    resource_name: str,
    fetcher: ActivityResourceFetcher,
    errors: dict[str, str],
) -> Any:
    try:
        return fetcher(api, activity_id)
    except GarminConnectConnectionError as exc:
        errors[resource_name] = str(exc)
        return None


def _build_activity_payload(api: Garmin, activity: dict[str, Any]) -> dict[str, Any]:
    activity_id = activity.get("activityId")
    
    payload: dict[str, Any] = {
        "activity_id": activity_id,
        "summary": activity,
    }
    errors: dict[str, str] = {}

    if activity_id is None:
        payload["errors"] = {
            "activity": "Garmin activity search response did not include activityId"
        }
        return payload

    # activity_id_str = str(activity_id)
    # for resource_name, fetcher in ACTIVITY_RESOURCE_FETCHERS:
    #     payload[resource_name] = _safe_fetch_activity_resource(
    #         api=api,
    #         activity_id=activity_id_str,
    #         resource_name=resource_name,
    #         fetcher=fetcher,
    #         errors=errors,
    #     )

    if errors:
        payload["errors"] = errors

    return payload


def _day_cache_key(day: date) -> str:
    """Return the cache key for a single day's activities."""
    return get_cache_key("activities", day.isoformat())


def _iter_days(start_date: date, end_date: date) -> list[date]:
    """Return every date in the inclusive [start_date, end_date] range."""
    return [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]


def _find_uncached_ranges(days: list[date]) -> tuple[list[date], list[tuple[date, date]]]:
    """Partition days into cached hits and contiguous uncached sub-ranges.

    Returns (cached_days, uncached_ranges) where uncached_ranges is a list of
    (start, end) pairs suitable for Garmin API calls.
    """
    cached_days: list[date] = []
    uncached_days: list[date] = []

    for day in days:
        cached = load_cached_data(_day_cache_key(day))
        if isinstance(cached, list):
            cached_days.append(day)
        else:
            uncached_days.append(day)

    # Group uncached days into contiguous sub-ranges
    uncached_ranges: list[tuple[date, date]] = []
    for day in uncached_days:
        if uncached_ranges and day == uncached_ranges[-1][1] + timedelta(days=1):
            uncached_ranges[-1] = (uncached_ranges[-1][0], day)
        else:
            uncached_ranges.append((day, day))

    return cached_days, uncached_ranges


def _activity_date(activity: dict[str, Any]) -> date | None:
    """Extract the local date from a Garmin activity summary."""
    start_local = activity.get("startTimeLocal")
    if isinstance(start_local, str) and len(start_local) >= 10:
        try:
            return date.fromisoformat(start_local[:10])
        except ValueError:
            return None
    return None


def _bucket_activities_by_day(
    activities: list[dict[str, Any]],
    range_days: list[date],
) -> dict[date, list[dict[str, Any]]]:
    """Map activities into per-day buckets; initialise empty lists for all days."""
    buckets: dict[date, list[dict[str, Any]]] = {day: [] for day in range_days}
    for activity in activities:
        day = _activity_date(activity)
        if day is not None and day in buckets:
            buckets[day].append(activity)
    return buckets


def get_activities_for_date_range(
    start_date: date,
    end_date: date,
) -> list[dict[str, Any]]:
    """Return all available Garmin activity data for an inclusive date range.

    Caching is per-day so overlapping date ranges share cached results.
    Only days without cached data trigger Garmin API calls, grouped into the
    fewest contiguous sub-ranges possible.
    """
    all_days = _iter_days(start_date, end_date)
    cached_days, uncached_ranges = _find_uncached_ranges(all_days)

    # Collect already-cached day payloads
    result: list[dict[str, Any]] = []
    for day in cached_days:
        cached = load_cached_data(_day_cache_key(day))
        if isinstance(cached, list):
            result.extend(cached)

    if not uncached_ranges:
        return result

    garmin_api = auth_garmin()
    if not garmin_api:
        return result

    # Fetch each contiguous uncached sub-range and cache per-day
    for range_start, range_end in uncached_ranges:
        activities = garmin_api.get_activities_by_date(
            startdate=range_start.isoformat(),
            enddate=range_end.isoformat(),
        )

        range_days = _iter_days(range_start, range_end)
        buckets = _bucket_activities_by_day(activities, range_days)

        for day, day_activities in buckets.items():
            day_payload = [
                _build_activity_payload(garmin_api, a) for a in day_activities
            ]
            # save_cached_data(_day_cache_key(day), day_payload)
            result.extend(day_payload)

    return result


def auth_garmin() -> Garmin | None:
    """Initialise Garmin API, restoring saved tokens or logging in fresh."""

    tokenstore = os.getenv("GARMIN_TOKEN_STORE") or "~/.garminconnect"
    tokenstore_path = str(Path(tokenstore).expanduser())

    # Try to restore saved tokens
    try:
        garmin = Garmin()
        garmin.login(tokenstore_path)
        print("Authenticated using saved tokens.")
        return garmin

    except GarminConnectTooManyRequestsError as err:
        print(f"Rate limit: {err}")
        sys.exit(1)

    except (GarminConnectAuthenticationError, GarminConnectConnectionError):
        print("No valid tokens found. Proceeding to login...")

    # Fresh credential login with MFA support
    while True:
        try:
            email = os.getenv("GARMIN_EMAIL")
            password = os.getenv("GARMIN_PASSWORD")

            if not email or not password:
                raise RuntimeError(
                    "GARMIN_EMAIL and GARMIN_PASSWORD must be set in the environment or .env file."
                )

            garmin = Garmin(
                email=email,
                password=password,
                prompt_mfa=lambda: input("MFA code: ").strip(),
            )
            garmin.login(tokenstore_path)
            print(f"Login successful. Tokens saved to: {tokenstore_path}")
            return garmin

        except GarminConnectTooManyRequestsError as err:
            print(f"Rate limit: {err}")
            sys.exit(1)

        except GarminConnectAuthenticationError:
            print("Wrong credentials.")
            return None

        except GarminConnectConnectionError as err:
            print(f"Connection error: {err}")
            return None

        except KeyboardInterrupt:
            return None
