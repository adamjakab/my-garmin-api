"""Helpers for transforming Garmin activity detail payloads."""

from typing import Any


METRICS_AGGREGATION_INTERVAL = 60  # seconds


def aggregate_activity_details(
    details: dict[str, Any],
    interval_seconds: int = METRICS_AGGREGATION_INTERVAL,
) -> dict[str, Any]:
    """Aggregate columnar activity detail metrics into time buckets with stats.

    Transforms raw Garmin metrics from columnar format (indexed arrays) into
    a keyed format with min/max/avg stats per time bucket.
    """
    if not details or "metricDescriptors" not in details or "activityDetailMetrics" not in details:
        return {"aggregationInterval": interval_seconds, "metrics": {}}

    descriptors = details.get("metricDescriptors", [])
    key_index_map: dict[str, int] = {}
    for desc in descriptors:
        if "key" in desc and "metricsIndex" in desc:
            key_index_map[desc["key"]] = desc["metricsIndex"]

    timestamp_index = key_index_map.get("directTimestamp")
    buckets: dict[int, dict[str, list[float]]] = {}
    activity_metrics = details.get("activityDetailMetrics", [])

    for measurement in activity_metrics:
        metric_values = measurement.get("metrics", [])
        if not metric_values or timestamp_index is None:
            continue

        timestamp_ms = metric_values[timestamp_index]
        if timestamp_ms is None:
            continue

        bucket_ts = int((timestamp_ms // (interval_seconds * 1000)) * (interval_seconds * 1000))
        if bucket_ts not in buckets:
            buckets[bucket_ts] = {}

        for key, index in key_index_map.items():
            if index < len(metric_values):
                value = metric_values[index]
                if value is not None:
                    if key not in buckets[bucket_ts]:
                        buckets[bucket_ts][key] = []
                    buckets[bucket_ts][key].append(value)

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
