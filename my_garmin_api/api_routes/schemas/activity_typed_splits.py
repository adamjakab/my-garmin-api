"""Activity typed splits schema models."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ActivityUuidSchema(BaseModel):
    uuid: Optional[str] = Field(
        default=None,
        title="Activity UUID",
        description="Stable Garmin UUID associated with the activity.",
    )


class TypedSplitSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    averageHR: Optional[float] = None
    averageSpeed: Optional[float] = None
    bmrCalories: Optional[float] = None
    calories: Optional[float] = None
    distance: Optional[float] = None
    duration: Optional[float] = None
    elapsedDuration: Optional[float] = None
    endTimeGMT: Optional[str] = None
    lapIndexes: Optional[list[int]] = None
    maxHR: Optional[float] = None
    messageIndex: Optional[int] = None
    movingDuration: Optional[float] = None
    startTimeGMT: Optional[str] = None
    startTimeLocal: Optional[str] = None
    totalExerciseReps: Optional[int] = None
    type: Optional[str] = None


class ActivityTypedSplitsSchema(BaseModel):
    activityId: Optional[int] = Field(
        default=None,
        title="Activity ID",
        description="Unique Garmin activity identifier for this typed split payload.",
    )

    activityUUID: Optional[ActivityUuidSchema] = Field(
        default=None,
        title="Activity UUID",
        description="UUID envelope for the activity this typed split payload belongs to.",
    )

    splits: Optional[list[TypedSplitSchema]] = Field(
        default=None,
        title="Typed Splits",
        description="Workout-phase splits such as active and rest intervals with per-phase metrics.",
    )
