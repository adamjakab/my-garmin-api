"""Garmin activity data aggregation helpers."""

import os
from datetime import date
from pathlib import Path
import sys
from typing import Any, Optional


from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)
from my_garmin_api.api_routes.schemas.activities import ActivitiesResponseSchema
from my_garmin_api.api_routes.schemas.activity import ActivitySchema
from my_garmin_api.helpers.activity_enrichment import enrich_activity_payload


def get_activity_by_id(activity_id: str) -> Optional[ActivitySchema]:
    """Return full details for a single activity by ID.

    Returns a dict with 'activity_id', 'summary', and 'splits' keys, or None if not found.
    """
    garmin_api = auth_garmin()
    if not garmin_api:
        return None

    try:
        activity = garmin_api.get_activity(activity_id)
        if not activity:
            return None

        # Flatten the nested structure from get_activity() to match schema expectations
        # The single activity endpoint returns summaryDTO with metrics, while batch endpoint flattens them
        flat_activity = dict(activity)

        # Merge summaryDTO fields to top level
        if "summaryDTO" in flat_activity:
            flat_activity.update(flat_activity.pop("summaryDTO"))

        # Normalize field names: activityTypeDTO -> activityType
        if "activityTypeDTO" in flat_activity:
            flat_activity["activityType"] = flat_activity.pop("activityTypeDTO")

        payload: dict[str, Any] = {
            "activity_id": activity_id,
            "summary": flat_activity,
        }

        # Enrich the payload with additional resources
        payload = enrich_activity_payload(garmin_api, payload, "details")
        payload = enrich_activity_payload(garmin_api, payload, "splits")
        payload = enrich_activity_payload(garmin_api, payload, "typed_splits")
        payload = enrich_activity_payload(garmin_api, payload, "split_summaries")
        payload = enrich_activity_payload(garmin_api, payload, "exercise_sets")
        payload = enrich_activity_payload(garmin_api, payload, "hr_time_in_zones")
        payload = enrich_activity_payload(garmin_api, payload, "power_time_in_zones")
        payload = enrich_activity_payload(garmin_api, payload, "weather")
        payload = enrich_activity_payload(garmin_api, payload, "gear")

        return ActivitySchema.model_validate(payload)

    except GarminConnectConnectionError:
        return None


def get_activities_for_date_range(
    start_date: date,
    end_date: date,
) -> ActivitiesResponseSchema:
    """Return all available Garmin activity data (summary only) for an inclusive date range.
    If any errors were encountered during fetching, an 'errors' key will be included with details.
    """
    garmin_api = auth_garmin()
    if not garmin_api:
        return ActivitiesResponseSchema(
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            count=0,
            activities=[],
        )

    activities = garmin_api.get_activities_by_date(
        startdate=start_date.isoformat(),
        enddate=end_date.isoformat(),
    )

    result: list[ActivitySchema] = []
    for activity in activities:
        activity_id = activity.get("activityId")
        payload: dict[str, Any] = {
            "activity_id": activity_id,
            "summary": activity,
        }

        if activity_id is None:
            payload["errors"] = {"activity": "Garmin activity search response did not include activityId"}

        result.append(ActivitySchema.model_validate(payload))

    return ActivitiesResponseSchema(
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        count=len(result),
        activities=result,
    )


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
                raise RuntimeError("GARMIN_EMAIL and GARMIN_PASSWORD must be set in the environment or .env file.")

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
