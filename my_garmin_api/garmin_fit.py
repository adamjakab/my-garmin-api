"""Garmin activity data aggregation helpers."""

import os
from collections.abc import Callable
from datetime import date
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
    ("activity", lambda api, activity_id: api.get_activity(activity_id)),
    ("details", lambda api, activity_id: api.get_activity_details(activity_id)),
    ("splits", lambda api, activity_id: api.get_activity_splits(activity_id)),
    (
        "typed_splits",
        lambda api, activity_id: api.get_activity_typed_splits(activity_id),
    ),
    (
        "split_summaries",
        lambda api, activity_id: api.get_activity_split_summaries(activity_id),
    ),
    ("weather", lambda api, activity_id: api.get_activity_weather(activity_id)),
    (
        "hr_time_in_zones",
        lambda api, activity_id: api.get_activity_hr_in_timezones(activity_id),
    ),
    (
        "power_time_in_zones",
        lambda api, activity_id: api.get_activity_power_in_timezones(activity_id),
    ),
    (
        "exercise_sets",
        lambda api, activity_id: api.get_activity_exercise_sets(activity_id),
    ),
    ("gear", lambda api, activity_id: api.get_activity_gear(activity_id)),
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

    activity_id_str = str(activity_id)
    for resource_name, fetcher in ACTIVITY_RESOURCE_FETCHERS:
        payload[resource_name] = _safe_fetch_activity_resource(
            api=api,
            activity_id=activity_id_str,
            resource_name=resource_name,
            fetcher=fetcher,
            errors=errors,
        )

    if errors:
        payload["errors"] = errors

    return payload


def get_activities_for_date_range(
    start_date: date,
    end_date: date,
) -> list[dict[str, Any]]:
    """Return all available Garmin activity data for an inclusive date range."""
    cache_key = get_cache_key("activities", start_date.isoformat(), end_date.isoformat())
    cached_activities = load_cached_data(cache_key)
    if isinstance(cached_activities, list):
        return cached_activities

    garmin_api = auth_garmin()
    if not garmin_api:
        return []

    activities = garmin_api.get_activities_by_date(
        startdate=start_date.isoformat(),
        enddate=end_date.isoformat(),
    )

    activity_payload = [
        _build_activity_payload(garmin_api, activity) for activity in activities
    ]
    save_cached_data(cache_key, activity_payload)

    return activity_payload


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
