"""Activity details schema models."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


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


class MetricsSchema(BaseModel):
    """Known Garmin metric keys with time-bucketed statistics. Additional keys are allowed."""

    model_config = ConfigDict(extra="allow")

    directHeartRate: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Heart Rate",
        description="Heart rate (bpm) per time bucket.",
    )

    directSpeed: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Speed",
        description="Speed (m/s) per time bucket.",
    )

    directRunCadence: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Running Cadence",
        description="Running cadence (steps/min) per time bucket. This is for one foot.",
    )

    directDoubleCadence: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Double Cadence",
        description="Double cadence (steps/min) per time bucket. This is for both feet.",
    )

    directFractionalCadence: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Fractional Cadence",
        description="Fractional cadence per time bucket.",
    )

    directPower: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Power",
        description="Power (W) per time bucket.",
    )

    directElevation: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Elevation",
        description="Elevation (m) per time bucket.",
    )

    directVerticalSpeed: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Vertical Speed",
        description="Vertical speed (m/s) per time bucket.",
    )

    directVerticalOscillation: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Vertical Oscillation",
        description="Vertical oscillation (cm) per time bucket.",
    )

    directVerticalRatio: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Vertical Ratio",
        description="Vertical ratio (%) per time bucket.",
    )

    directStrideLength: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Stride Length",
        description="Stride length (cm) per time bucket.",
    )

    directGroundContactTime: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Ground Contact Time",
        description="Ground contact time (ms) per time bucket.",
    )

    directGradeAdjustedSpeed: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Grade Adjusted Speed",
        description="Grade-adjusted speed (m/s) per time bucket.",
    )

    directAirTemperature: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Air Temperature",
        description="Air temperature (°C) per time bucket.",
    )

    directBodyBattery: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Body Battery",
        description="Body battery level per time bucket.",
    )

    directAvailableStamina: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Available Stamina",
        description="Available stamina (%) per time bucket.",
    )

    directPotentialStamina: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Potential Stamina",
        description="Potential stamina (%) per time bucket.",
    )

    directPerformanceCondition: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Performance Condition",
        description="Performance condition score per time bucket.",
    )

    directLatitude: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Latitude",
        description="GPS latitude (degrees) per time bucket.",
    )

    directLongitude: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Longitude",
        description="GPS longitude (degrees) per time bucket.",
    )

    sumDistance: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Distance",
        description="Cumulative distance (m) per time bucket.",
    )

    sumDuration: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Duration",
        description="Cumulative duration (s) per time bucket.",
    )

    sumElapsedDuration: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Elapsed Duration",
        description="Cumulative elapsed duration (s) per time bucket.",
    )

    sumMovingDuration: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Moving Duration",
        description="Cumulative moving duration (s) per time bucket.",
    )

    sumAccumulatedPower: Optional[list[MetricStatSchema]] = Field(
        default=None,
        title="Accumulated Power",
        description="Cumulative accumulated power (W) per time bucket.",
    )


class AggregatedDetailsSchema(BaseModel):
    """Aggregated activity detail metrics organized by metric key and time buckets."""

    aggregationInterval: int = Field(
        title="Aggregation Interval",
        description="Time interval in seconds for metric aggregation buckets.",
    )
    metrics: MetricsSchema = Field(
        title="Aggregated Metrics",
        description="Metrics keyed by metric name, each containing time-bucketed statistics.",
    )
