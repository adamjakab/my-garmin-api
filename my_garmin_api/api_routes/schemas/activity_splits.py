"""Activity splits schema models."""

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


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
    model_config = ConfigDict(extra="allow")

    averageHR: Optional[float] = Field(
        default=None,
        title="Lap Average Heart Rate",
        description="Average heart rate during the lap (beats per minute).",
    )
    averageMovingSpeed: Optional[float] = Field(
        default=None,
        title="Lap Average Moving Speed",
        description="Average moving speed during the lap (meters/second).",
    )
    averagePower: Optional[float] = Field(
        default=None,
        title="Lap Average Power",
        description="Average power during the lap (watts).",
    )
    averageRunCadence: Optional[float] = Field(
        default=None,
        title="Lap Average Run Cadence",
        description="Average running cadence during the lap (steps per minute).",
    )
    averageSpeed: Optional[float] = Field(
        default=None,
        title="Lap Average Speed",
        description="Average speed during the lap (meters/second).",
    )
    averageTemperature: Optional[float] = Field(
        default=None,
        title="Lap Average Temperature",
        description="Average skin temperature during the lap (Celsius).",
    )
    avgGradeAdjustedSpeed: Optional[float] = Field(
        default=None,
        title="Lap Average Grade Adjusted Speed",
        description="Average grade adjusted speed during the lap (meters/second).",
    )
    bmrCalories: Optional[float] = Field(
        default=None,
        title="Lap BMR Calories",
        description="Basal metabolic rate calories burned during the lap (kcal).",
    )
    calories: Optional[float] = Field(
        default=None,
        title="Lap Calories",
        description="Total calories burned during the lap (kcal).",
    )
    connectIQMeasurement: Optional[list[dict[str, Any]]] = Field(
        default=None,
        title="Lap Connect IQ Measurements",
        description="Custom measurements from Connect IQ apps during the lap.",
    )
    directWorkoutComplianceScore: Optional[int] = Field(
        default=None,
        title="Lap Direct Workout Compliance Score",
        description="Compliance score for how well the planned workout was followed during the lap (percentage).",
    )
    distance: Optional[float] = Field(
        default=None,
        title="Lap Distance",
        description="Total distance covered in this lap (meters).",
    )
    duration: Optional[float] = Field(
        default=None,
        title="Lap Duration",
        description="Total elapsed time for this lap (seconds).",
    )
    elapsedDuration: Optional[float] = Field(
        default=None,
        title="Lap Elapsed Duration",
        description="Total elapsed time for this lap including pauses (seconds).",
    )
    elevationGain: Optional[float] = Field(
        default=None,
        title="Lap Elevation Gain",
        description="Total elevation gain during the lap (meters).",
    )
    elevationLoss: Optional[float] = Field(
        default=None,
        title="Lap Elevation Loss",
        description="Total elevation loss during the lap (meters).",
    )
    endLatitude: Optional[float] = Field(
        default=None,
        title="Lap End Latitude",
        description="Latitude at the end of the lap (degrees).",
    )
    endLongitude: Optional[float] = Field(
        default=None,
        title="Lap End Longitude",
        description="Longitude at the end of the lap (degrees).",
    )
    groundContactTime: Optional[float] = Field(
        default=None,
        title="Lap Ground Contact Time",
        description="Average ground contact time during the lap (milliseconds).",
    )
    intensityType: Optional[str] = Field(
        default=None,
        title="Lap Intensity Type",
        description="Intensity type for the lap.",
    )
    lapIndex: Optional[int] = Field(
        default=None,
        title="Lap Index",
        description="Index of the lap or split within the activity.",
    )
    lengthDTOs: Optional[list[dict[str, Any]]] = Field(
        default=None,
        title="Lap Length DTOs",
        description="Detailed length metrics for the lap.",
    )
    maxElevation: Optional[float] = Field(
        default=None,
        title="Lap Max Elevation",
        description="Maximum elevation during the lap (meters).",
    )
    maxHR: Optional[float] = Field(
        default=None,
        title="Lap Max Heart Rate",
        description="Maximum heart rate during the lap (beats per minute).",
    )
    maxPower: Optional[float] = Field(
        default=None,
        title="Lap Max Power",
        description="Maximum power during the lap (watts).",
    )
    maxRunCadence: Optional[float] = Field(
        default=None,
        title="Lap Max Run Cadence",
        description="Maximum running cadence during the lap (steps per minute).",
    )
    maxSpeed: Optional[float] = Field(
        default=None,
        title="Lap Max Speed",
        description="Maximum speed during the lap (meters/second).",
    )
    maxTemperature: Optional[float] = Field(
        default=None,
        title="Lap Max Temperature",
        description="Maximum skin temperature during the lap (Celsius).",
    )
    maxVerticalSpeed: Optional[float] = Field(
        default=None,
        title="Lap Max Vertical Speed",
        description="Maximum vertical speed during the lap (meters/second).",
    )
    messageIndex: Optional[int] = Field(
        default=None,
        title="Lap Message Index",
        description="Index of the lap message in the original FIT file.",
    )
    minElevation: Optional[float] = Field(
        default=None,
        title="Lap Min Elevation",
        description="Minimum elevation during the lap (meters).",
    )
    minPower: Optional[float] = Field(
        default=None,
        title="Lap Min Power",
        description="Minimum power during the lap (watts).",
    )
    minTemperature: Optional[float] = Field(
        default=None,
        title="Lap Min Temperature",
        description="Minimum skin temperature during the lap (Celsius).",
    )
    movingDuration: Optional[float] = Field(
        default=None,
        title="Lap Moving Duration",
        description="Total moving time for this lap (seconds).",
    )
    normalizedPower: Optional[float] = Field(
        default=None,
        title="Lap Normalized Power",
        description="Normalized power for the lap (watts).",
    )
    startLatitude: Optional[float] = Field(
        default=None,
        title="Lap Start Latitude",
        description="Latitude at the start of the lap (degrees).",
    )
    startLongitude: Optional[float] = Field(
        default=None,
        title="Lap Start Longitude",
        description="Longitude at the start of the lap (degrees).",
    )
    startTimeGMT: Optional[str] = Field(
        default=None,
        title="Lap Start Time GMT",
        description="Start time of the lap/split in GMT.",
    )
    strideLength: Optional[float] = Field(
        default=None,
        title="Lap Stride Length",
        description="Average stride length during the lap (centimeters).",
    )
    totalWork: Optional[float] = Field(
        default=None,
        title="Lap Total Work",
        description="Total work done during the lap (kilojoules).",
    )
    verticalOscillation: Optional[float] = Field(
        default=None,
        title="Lap Vertical Oscillation",
        description="Vertical oscillation during the lap (centimeters).",
    )
    verticalRatio: Optional[float] = Field(
        default=None,
        title="Lap Vertical Ratio",
        description="Vertical ratio during the lap (percentage).",
    )
    wktIndex: Optional[int] = Field(
        default=None,
        title="Lap WKT Index",
        description="Index of the lap in the workout template.",
    )
    wktStepIndex: Optional[int] = Field(
        default=None,
        title="Lap WKT Step Index",
        description="Index of the lap step in the workout template.",
    )


class ActivitySplitsSchema(BaseModel):
    activityId: Optional[int] = Field(
        default=None,
        title="Activity ID",
        description="Unique Garmin activity identifier for this split payload.",
    )

    lapDTOs: Optional[list[LapSchema]] = Field(
        default=None,
        title="Laps",
        description=(
            "Per-lap metrics for the activity. "
            "Laps can be auto-generated by Garmin based on distance or manually triggered by the user. "
            "Typically, laps are emitted at regular distance intervals (e.g. every 1 km during runs)."
        ),
    )

    eventDTOs: Optional[list[SplitEventSchema]] = Field(
        default=None,
        title="Events",
        description=(
            "Events emitted during the activity. "
            "These can include automatic events like warnings for heart rate or pace being outside of the planned range."
        ),
    )
