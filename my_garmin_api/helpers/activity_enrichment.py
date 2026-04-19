"""Helpers for enriching activity payloads with Garmin activity resources."""

from typing import Any, Callable, Literal

from garminconnect import Garmin

from my_garmin_api.helpers.activity_details import aggregate_activity_details


ActivityResourceFetcher = Callable[[Garmin, str], Any]
ActivityResourceName = Literal[
    "details",
    "splits",
    "typed_splits",
    "split_summaries",
    "exercise_sets",
    "hr_time_in_zones",
    "power_time_in_zones",
    "weather",
    "gear",
]

ACTIVITY_RESOURCE_FETCHERS: dict[ActivityResourceName, ActivityResourceFetcher] = {
    "details": lambda api, activity_id: aggregate_activity_details(api.get_activity_details(activity_id)),
    "splits": lambda api, activity_id: api.get_activity_splits(activity_id),
    "typed_splits": lambda api, activity_id: api.get_activity_typed_splits(activity_id),
    "split_summaries": lambda api, activity_id: api.get_activity_split_summaries(activity_id),
    "exercise_sets": lambda api, activity_id: api.get_activity_exercise_sets(activity_id),
    "hr_time_in_zones": lambda api, activity_id: api.get_activity_hr_in_timezones(activity_id),
    "power_time_in_zones": lambda api, activity_id: api.get_activity_power_in_timezones(activity_id),
    "weather": lambda api, activity_id: api.get_activity_weather(activity_id),
    "gear": lambda api, activity_id: api.get_activity_gear(activity_id),
}


def enrich_activity_payload(
    garmin_api: Garmin,
    payload: dict[str, Any],
    resource_name: ActivityResourceName,
) -> dict[str, Any]:
    """Return an activity payload enriched with the requested Garmin resource."""
    activity_id = payload.get("activity_id")
    if activity_id is None:
        raise ValueError("Activity payload must include a top-level activity_id.")

    fetcher = ACTIVITY_RESOURCE_FETCHERS.get(resource_name)
    if fetcher is None:
        raise ValueError(f"Unsupported activity resource: {resource_name}")

    enriched_activity = dict(payload)
    enriched_activity[resource_name] = fetcher(garmin_api, str(activity_id))
    return enriched_activity
