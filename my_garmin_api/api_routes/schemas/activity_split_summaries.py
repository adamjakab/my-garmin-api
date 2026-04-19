"""Activity split summaries schema models."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .activity_typed_splits import ActivityUuidSchema


class SplitSummarySchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    distance: Optional[float] = None
    duration: Optional[float] = None
    movingDuration: Optional[float] = None
    averageSpeed: Optional[float] = None
    calories: Optional[float] = None
    bmrCalories: Optional[float] = None
    averageHR: Optional[float] = None
    maxHR: Optional[float] = None
    totalExerciseReps: Optional[int] = None
    splitType: Optional[str] = None
    noOfSplits: Optional[int] = None
    maxDistance: Optional[float] = None
    maxDistanceWithPrecision: Optional[float] = None


class ActivitySplitSummariesSchema(BaseModel):
    activityId: Optional[int] = Field(
        default=None,
        title="Activity ID",
        description="Unique Garmin activity identifier for this split summaries payload.",
    )

    activityUUID: Optional[ActivityUuidSchema] = Field(
        default=None,
        title="Activity UUID",
        description="UUID envelope for the activity this split summaries payload belongs to.",
    )

    splitSummaries: Optional[list[SplitSummarySchema]] = Field(
        default=None,
        title="Split Summaries",
        description="Aggregate metrics grouped by split type, such as active and rest intervals.",
    )
