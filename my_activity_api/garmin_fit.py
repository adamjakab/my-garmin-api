"""Garmin workout data aggregation helpers."""

import json
import os
from collections.abc import Callable
from datetime import date
from pathlib import Path
import sys
from typing import Any


from .garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)


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


def _build_workout_payload(api: Garmin, activity: dict[str, Any]) -> dict[str, Any]:
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


def get_workouts_for_date(
    workout_date: date | None = None,
    api: Garmin | None = None,
) -> list[dict[str, Any]]:
    """Return all available Garmin workout data for a single day."""
    if workout_date is None:
        workout_date = date.today()

    garmin_api = api or init_api()
    if not garmin_api:
        return []

    activities = garmin_api.get_activities_by_date(
        startdate=workout_date.isoformat(),
        enddate=workout_date.isoformat(),
    )
    return [_build_workout_payload(garmin_api, activity) for activity in activities]


def do_it(workout_date: date | None = None, tmp_dir: str = "tmp") -> list[dict[str, Any]]:
    """Fetch workouts for a day and print them as JSON."""
    _ = tmp_dir

    api = init_api()
    if not api:
        return []

    if workout_date is None:
        workout_date = date.today()

    full_name = api.get_full_name() or ""
    first_name = full_name.split()[0] if full_name.strip() else "Unknown User"
    print(f"Welcome to Garmin. You are: {first_name}.")

    workouts = get_workouts_for_date(workout_date=workout_date, api=api)
    print(json.dumps(workouts, indent=2))
    return workouts

def init_api() -> Garmin | None:
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
