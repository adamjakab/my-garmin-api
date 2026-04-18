"""Garmin activity data aggregation helpers."""

import os
from datetime import date
from pathlib import Path
import sys
from typing import Any


from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)


# ACTIVITY_RESOURCE_FETCHERS: tuple[tuple[str, ActivityResourceFetcher], ...] = (
#     ("activity", lambda api, activity_id: api.get_activity(activity_id)),
#     ("details", lambda api, activity_id: api.get_activity_details(activity_id)),
#
#   ("splits", lambda api, activity_id: api.get_activity_splits(activity_id)),
#     (
#         "typed_splits",
#         lambda api, activity_id: api.get_activity_typed_splits(activity_id),
#     ),
#     (
#         "split_summaries",
#         lambda api, activity_id: api.get_activity_split_summaries(activity_id),
#     ),
#     ("weather", lambda api, activity_id: api.get_activity_weather(activity_id)),
#     (
#         "hr_time_in_zones",
#         lambda api, activity_id: api.get_activity_hr_in_timezones(activity_id),
#     ),
#     (
#         "power_time_in_zones",
#         lambda api, activity_id: api.get_activity_power_in_timezones(activity_id),
#     ),
#     (
#         "exercise_sets",
#         lambda api, activity_id: api.get_activity_exercise_sets(activity_id),
#     ),
#     ("gear", lambda api, activity_id: api.get_activity_gear(activity_id)),
# )

METRICS_AGGREGATION_INTERVAL = 60  # seconds


def _aggregate_activity_details(
    details: dict[str, Any],
    interval_seconds: int = METRICS_AGGREGATION_INTERVAL,
) -> dict[str, Any]:
    """Aggregate columnar activity detail metrics into time buckets with stats.

    Transforms raw Garmin metrics from columnar format (indexed arrays) into
    a keyed format with min/max/avg stats per time bucket.
    """
    if not details or "metricDescriptors" not in details or "activityDetailMetrics" not in details:
        return {"aggregationInterval": interval_seconds, "metrics": {}}

    # Build key -> index map from descriptors
    descriptors = details.get("metricDescriptors", [])
    key_index_map: dict[str, int] = {}
    for desc in descriptors:
        if "key" in desc and "metricsIndex" in desc:
            key_index_map[desc["key"]] = desc["metricsIndex"]

    # Find timestamp index (usually directTimestamp at index 1)
    timestamp_index = key_index_map.get("directTimestamp")

    # Aggregate metrics into buckets
    buckets: dict[int, dict[str, list[float]]] = {}  # bucket_ts -> metric_key -> list of values
    activity_metrics = details.get("activityDetailMetrics", [])

    for measurement in activity_metrics:
        metric_values = measurement.get("metrics", [])
        if not metric_values or timestamp_index is None:
            continue

        # Get timestamp and bucket it
        timestamp_ms = metric_values[timestamp_index]
        if timestamp_ms is None:
            continue
        bucket_ts = int((timestamp_ms // (interval_seconds * 1000)) * (interval_seconds * 1000))

        if bucket_ts not in buckets:
            buckets[bucket_ts] = {}

        # Store metric values in their bucket
        for key, index in key_index_map.items():
            if index < len(metric_values):
                value = metric_values[index]
                if value is not None:
                    if key not in buckets[bucket_ts]:
                        buckets[bucket_ts][key] = []
                    buckets[bucket_ts][key].append(value)

    # Calculate stats per bucket and metric
    metrics_output: dict[str, list[dict[str, Any]]] = {}
    for bucket_ts in sorted(buckets.keys()):
        bucket_data = buckets[bucket_ts]
        for key, values in bucket_data.items():
            if key not in metrics_output:
                metrics_output[key] = []

            if values:
                avg_val = sum(values) / len(values)
                metrics_output[key].append(
                    {
                        "timestamp": bucket_ts,
                        "min": min(values),
                        "max": max(values),
                        "avg": avg_val,
                        "count": len(values),
                    }
                )

    return {
        "aggregationInterval": interval_seconds,
        "metrics": metrics_output,
    }


def get_activity_by_id(activity_id: str) -> dict[str, Any] | None:
    """Return full details for a single activity by ID.

    Returns a dict with 'activity_id', 'summary', and 'details' keys, or None if not found.
    The 'details' contains aggregated metrics organized by time buckets with min/max/avg stats.
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

        # Get activity details and aggregate metrics
        raw_details = garmin_api.get_activity_details(activity_id)
        aggregated_details = _aggregate_activity_details(raw_details) if raw_details else None

        # Get activity splits
        splits = garmin_api.get_activity_splits(activity_id)

        payload: dict[str, Any] = {
            "activity_id": activity_id,
            "summary": flat_activity,
            # "details": aggregated_details,
            "splits": splits,
        }
        return payload
    except GarminConnectConnectionError:
        return None


def get_activities_for_date_range(
    start_date: date,
    end_date: date,
) -> list[dict[str, Any]]:
    """Return all available Garmin activity data (summary only) for an inclusive date range.
    Each activity is represented as a dict with at least an 'activity_id' and 'summary' key.
    The 'summary' value is the raw activity data returned by Garmin Connect API.
    If any errors were encountered during fetching, an 'errors' key will be included with details.
    """
    garmin_api = auth_garmin()
    if not garmin_api:
        return []

    activities = garmin_api.get_activities_by_date(
        startdate=start_date.isoformat(),
        enddate=end_date.isoformat(),
    )

    result = []
    for activity in activities:
        activity_id = activity.get("activityId")
        payload: dict[str, Any] = {
            "activity_id": activity_id,
            "summary": activity,
        }
        errors: dict[str, str] = {}

        if activity_id is None:
            payload["errors"] = {"activity": "Garmin activity search response did not include activityId"}
            result.append(payload)
            continue

        if errors:
            payload["errors"] = errors

        result.append(payload)

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
