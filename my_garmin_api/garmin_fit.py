"""Garmin activity data aggregation helpers."""

import os
from datetime import date, timedelta
from pathlib import Path
import sys
from typing import Any, Dict, Optional


from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)
from my_garmin_api.helpers.activity_enrichment import ActivityResourceName, enrich_activity_payload


def get_activity_by_id(
    activity_id: str,
    enabled_enrichments: Optional[set[ActivityResourceName]] = None,
) -> Optional[Dict[str, Any]]:
    """Return full details for a single activity by ID.

    Returns a dict with 'activity_id', 'summary', and enrichment keys, or None if not found.
    When *enabled_enrichments* is provided, only those resources are fetched; all others are
    skipped.  Pass ``None`` (default) to fetch every resource.
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
        all_resources: list[ActivityResourceName] = [
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
        for resource in all_resources:
            if enabled_enrichments is None or resource in enabled_enrichments:
                payload = enrich_activity_payload(garmin_api, payload, resource)

        return payload

    except GarminConnectConnectionError:
        return None


def get_activities_for_date_range(
    start_date: date,
    end_date: date,
) -> Optional[Dict[str, Any]]:
    """Return all available Garmin activity data (summary only) for an inclusive date range.
    If any errors were encountered during fetching, an 'errors' key will be included with details.
    """
    garmin_api = auth_garmin()
    if not garmin_api:
        return None

    activities = garmin_api.get_activities_by_date(
        startdate=start_date.isoformat(),
        enddate=end_date.isoformat(),
    )

    result: list[Dict[str, Any]] = []
    for activity in activities:
        activity_id = activity.get("activityId")
        payload: dict[str, Any] = {
            "activity_id": activity_id,
            "summary": activity,
        }

        if activity_id is None:
            payload["errors"] = {"activity": "Garmin activity search response did not include activityId"}

        result.append(payload)

    return {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "count": len(result),
        "activities": result,
    }


def get_hrv_for_date_range(
    from_date: date,
    to_date: date,
) -> Optional[Dict[str, Any]]:
    """Return HRV data for the provided inclusive date range."""
    garmin_api = auth_garmin()
    if not garmin_api:
        return None

    try:
        result: list[Dict[str, Any]] = []
        current = from_date
        while current <= to_date:
            hrv_data = garmin_api.get_hrv_data(current.isoformat())
            if hrv_data is not None:
                # Drop high-volume samples from API output while preserving summary-level HRV fields.
                sanitized_hrv_data = dict(hrv_data)
                sanitized_hrv_data.pop("hrvReadings", None)
                result.append(
                    {
                        "date": current.isoformat(),
                        "hrv": sanitized_hrv_data,
                    }
                )
            current += timedelta(days=1)

        return {
            "start_date": from_date.isoformat(),
            "end_date": to_date.isoformat(),
            "count": len(result),
            "hrv_data": result,
        }
    except GarminConnectConnectionError:
        return None


def get_rhr_for_date_range(
    from_date: date,
    to_date: date,
) -> Optional[Dict[str, Any]]:
    """Return resting heart rate data for the provided inclusive date range."""
    garmin_api = auth_garmin()
    if not garmin_api:
        return None

    try:
        result: list[Dict[str, Any]] = []
        current = from_date
        while current <= to_date:
            rhr_data = garmin_api.get_rhr_day(current.isoformat())
            if rhr_data is not None:
                result.append(
                    {
                        "date": current.isoformat(),
                        "rhr": rhr_data,
                    }
                )
            current += timedelta(days=1)

        return {
            "start_date": from_date.isoformat(),
            "end_date": to_date.isoformat(),
            "count": len(result),
            "rhr_data": result,
        }
    except GarminConnectConnectionError:
        return None


def get_weight_for_date_range(
    from_date: date,
    to_date: date,
) -> Optional[Dict[str, Any]]:
    """Return weight/body composition measurements for the provided inclusive date range."""
    garmin_api = auth_garmin()
    if not garmin_api:
        return None

    try:
        body_composition = garmin_api.get_body_composition(
            startdate=from_date.isoformat(),
            enddate=to_date.isoformat(),
        )

        measurements = body_composition.get("dateWeightList", [])
        if not isinstance(measurements, list):
            measurements = []

        result: list[Dict[str, Any]] = []
        for measurement in measurements:
            if not isinstance(measurement, dict):
                continue

            measurement_date = measurement.get("calendarDate")
            if not isinstance(measurement_date, str) or not measurement_date:
                measurement_date = from_date.isoformat()

            result.append(
                {
                    "date": measurement_date,
                    "weight": measurement,
                }
            )

        return {
            "start_date": from_date.isoformat(),
            "end_date": to_date.isoformat(),
            "count": len(result),
            "weight_data": result,
        }
    except GarminConnectConnectionError:
        return None


def get_sleep_for_date_range(
    from_date: date,
    to_date: date,
) -> Optional[Dict[str, Any]]:
    """Return sleep data for the provided inclusive date range."""
    garmin_api = auth_garmin()
    if not garmin_api:
        return None

    try:
        result: list[Dict[str, Any]] = []
        current = from_date
        while current <= to_date:
            sleep_data = garmin_api.get_sleep_data(current.isoformat())
            if sleep_data is not None:
                score_value = None
                duration_seconds = None
                if isinstance(sleep_data, dict):
                    daily_sleep = sleep_data.get("dailySleepDTO")
                    if isinstance(daily_sleep, dict):
                        duration_seconds = daily_sleep.get("sleepTimeSeconds")

                        sleep_scores = daily_sleep.get("sleepScores")
                        if isinstance(sleep_scores, dict):
                            overall = sleep_scores.get("overall")
                            if isinstance(overall, dict):
                                score_value = overall.get("value")

                        if score_value is None:
                            legacy_score = daily_sleep.get("sleepScore")
                            if isinstance(legacy_score, dict):
                                score_value = legacy_score.get("overallScore")

                    if duration_seconds is None:
                        duration_seconds = sleep_data.get("sleepTimeSeconds")

                    if score_value is None:
                        legacy_top_score = sleep_data.get("sleepScore")
                        if isinstance(legacy_top_score, dict):
                            score_value = legacy_top_score.get("overallScore")

                if score_value is None and duration_seconds is None:
                    current += timedelta(days=1)
                    continue

                result.append(
                    {
                        "date": current.isoformat(),
                        "sleep": {
                            "score": score_value,
                            "duration_seconds": duration_seconds,
                        },
                    }
                )
            current += timedelta(days=1)

        return {
            "start_date": from_date.isoformat(),
            "end_date": to_date.isoformat(),
            "count": len(result),
            "sleep_data": result,
        }
    except GarminConnectConnectionError:
        return None


def _contains_vo2max_data(value: Any) -> bool:
    """Return True when payload contains a non-null VO2 max related field."""
    if isinstance(value, dict):
        for key, nested_value in value.items():
            normalized_key = str(key).lower()
            if "vo2" in normalized_key and nested_value is not None:
                return True
            if _contains_vo2max_data(nested_value):
                return True
        return False

    if isinstance(value, list):
        return any(_contains_vo2max_data(item) for item in value)

    return False


def _extract_vo2max_metrics(max_metrics_data: Any) -> list[dict[str, Any]]:
    """Extract VO2 max-related metric entries from Garmin max metrics payload."""
    candidate_metrics: list[Any] = []

    if isinstance(max_metrics_data, list):
        candidate_metrics = max_metrics_data
    elif isinstance(max_metrics_data, dict):
        metrics = max_metrics_data.get("maxMetrics")
        if isinstance(metrics, list):
            candidate_metrics = metrics
        else:
            candidate_metrics = [max_metrics_data]

    vo2max_metrics: list[dict[str, Any]] = []
    for metric in candidate_metrics:
        if not isinstance(metric, dict):
            continue

        if _contains_vo2max_data(metric):
            vo2max_metrics.append(metric)

    return vo2max_metrics


def _extract_metric_calendar_date(metric: dict[str, Any], fallback_date: date) -> date:
    """Resolve the most specific Garmin calendarDate for a VO2 metric record."""
    metric_date = metric.get("calendarDate")
    if isinstance(metric_date, str):
        try:
            return date.fromisoformat(metric_date)
        except ValueError:
            pass

    for nested_value in metric.values():
        if not isinstance(nested_value, dict):
            continue

        nested_date = nested_value.get("calendarDate")
        if not isinstance(nested_date, str):
            continue

        try:
            return date.fromisoformat(nested_date)
        except ValueError:
            continue

    return fallback_date


def _extract_vo2max_precise_values(value: Any) -> list[float]:
    """Collect all numeric vo2MaxPreciseValue entries from nested Garmin payloads."""
    values: list[float] = []

    if isinstance(value, dict):
        for key, nested_value in value.items():
            if str(key).lower() == "vo2maxprecisevalue" and isinstance(nested_value, (int, float)):
                values.append(float(nested_value))

            values.extend(_extract_vo2max_precise_values(nested_value))

    elif isinstance(value, list):
        for item in value:
            values.extend(_extract_vo2max_precise_values(item))

    return values


def get_vo2max_for_date_range(
    from_date: date,
    to_date: date,
) -> Optional[Dict[str, Any]]:
    """Return VO2 max data for the provided inclusive date range."""
    garmin_api = auth_garmin()
    if not garmin_api:
        return None

    try:
        precise_values_by_date: dict[str, list[float]] = {}
        current = from_date
        while current <= to_date:
            max_metrics_data = garmin_api.get_max_metrics(current.isoformat())
            vo2max_metrics = _extract_vo2max_metrics(max_metrics_data)

            for metric in vo2max_metrics:
                metric_calendar_date = _extract_metric_calendar_date(metric, current)
                if metric_calendar_date < from_date or metric_calendar_date > to_date:
                    continue

                precise_values = _extract_vo2max_precise_values(metric)
                if not precise_values:
                    continue

                metric_date_key = metric_calendar_date.isoformat()
                precise_values_by_date.setdefault(metric_date_key, []).extend(precise_values)

            current += timedelta(days=1)

        result: list[Dict[str, Any]] = []
        for metric_date in sorted(precise_values_by_date):
            result.append(
                {
                    "date": metric_date,
                    "vo2max_precise_value": max(precise_values_by_date[metric_date]),
                }
            )

        return {
            "start_date": from_date.isoformat(),
            "end_date": to_date.isoformat(),
            "count": len(result),
            "vo2max_data": result,
        }
    except GarminConnectConnectionError:
        return None


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
