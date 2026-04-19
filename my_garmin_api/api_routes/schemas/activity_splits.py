"""Activity splits schema models."""

from typing import Any, Optional

from pydantic import BaseModel, Field


class SplitSectionTypeSchema(BaseModel):
    id: Optional[int] = Field(
        default=None,
        title="Section Type ID",
        description="Numeric identifier for the split event section type.",
    )

    key: Optional[str] = Field(
        default=None,
        title="Section Type Key",
        description="Short key representing the section type.",
    )

    sectionTypeKey: Optional[str] = Field(
        default=None,
        title="Section Type Enum Key",
        description="Canonical enum-like section type key from Garmin.",
    )


class SplitEventSchema(BaseModel):
    startTimeGMT: Optional[str] = Field(
        default=None,
        title="Event Start Time GMT",
        description="Event timestamp in UTC, ISO 8601 format.",
    )

    startTimeGMTDoubleValue: Optional[float] = Field(
        default=None,
        title="Event Start Time GMT Milliseconds",
        description="Event start timestamp in Unix epoch milliseconds.",
    )

    sectionTypeDTO: Optional[SplitSectionTypeSchema] = Field(
        default=None,
        title="Section Type",
        description="Classification metadata for the event.",
    )


class LapSchema(BaseModel):
    model_config = {
        "extra": "ignore",
    }

    startTimeGMT: Optional[str] = None
    startLatitude: Optional[float] = None
    startLongitude: Optional[float] = None
    distance: Optional[float] = None
    duration: Optional[float] = None
    movingDuration: Optional[float] = None
    elapsedDuration: Optional[float] = None
    elevationGain: Optional[float] = None
    elevationLoss: Optional[float] = None
    maxElevation: Optional[float] = None
    minElevation: Optional[float] = None
    averageSpeed: Optional[float] = None
    averageMovingSpeed: Optional[float] = None
    maxSpeed: Optional[float] = None
    calories: Optional[float] = None
    bmrCalories: Optional[float] = None
    averageHR: Optional[float] = None
    maxHR: Optional[float] = None
    averageRunCadence: Optional[float] = None
    maxRunCadence: Optional[float] = None
    averageTemperature: Optional[float] = None
    maxTemperature: Optional[float] = None
    minTemperature: Optional[float] = None
    averagePower: Optional[float] = None
    maxPower: Optional[float] = None
    minPower: Optional[float] = None
    normalizedPower: Optional[float] = None
    totalWork: Optional[float] = None
    groundContactTime: Optional[float] = None
    strideLength: Optional[float] = None
    verticalOscillation: Optional[float] = None
    verticalRatio: Optional[float] = None
    endLatitude: Optional[float] = None
    endLongitude: Optional[float] = None
    maxVerticalSpeed: Optional[float] = None
    directWorkoutComplianceScore: Optional[int] = None
    avgGradeAdjustedSpeed: Optional[float] = None
    lapIndex: Optional[int] = None
    wktStepIndex: Optional[int] = None
    lengthDTOs: Optional[list[dict[str, Any]]] = None
    wktIndex: Optional[int] = None
    connectIQMeasurement: Optional[list[dict[str, Any]]] = None
    intensityType: Optional[str] = None
    messageIndex: Optional[int] = None


class ActivitySplitsSchema(BaseModel):
    activityId: Optional[int] = Field(
        default=None,
        title="Activity ID",
        description="Unique Garmin activity identifier for this split payload.",
    )

    lapDTOs: Optional[list[LapSchema]] = Field(
        default=None,
        title="Laps",
        description="Per-lap metrics for the activity.",
    )

    eventDTOs: Optional[list[SplitEventSchema]] = Field(
        default=None,
        title="Split Events",
        description="Split timeline events emitted during the activity.",
    )
