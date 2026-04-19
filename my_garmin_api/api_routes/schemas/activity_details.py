"""Activity details schema models."""

from typing import Optional

from pydantic import BaseModel, Field


class MetricStatSchema(BaseModel):
    """Statistics for a single metric within a time bucket."""

    timestamp: int = Field(
        title="Bucket Timestamp",
        description="Unix timestamp (ms) representing the start of the bucket.",
    )
    min: Optional[float] = Field(
        default=None,
        title="Minimum Value",
        description="Minimum value recorded in this bucket.",
    )
    max: Optional[float] = Field(
        default=None,
        title="Maximum Value",
        description="Maximum value recorded in this bucket.",
    )
    avg: Optional[float] = Field(
        default=None,
        title="Average Value",
        description="Average value recorded in this bucket.",
    )
    count: Optional[int] = Field(
        default=None,
        title="Count",
        description="Number of measurements in this bucket.",
    )


class AggregatedDetailsSchema(BaseModel):
    """Aggregated activity detail metrics organized by metric key and time buckets."""

    aggregationInterval: int = Field(
        title="Aggregation Interval",
        description="Time interval in seconds for metric aggregation buckets.",
    )
    metrics: dict[str, list[MetricStatSchema]] = Field(
        title="Aggregated Metrics",
        description="Metrics keyed by metric name, each containing time-bucketed statistics.",
    )
