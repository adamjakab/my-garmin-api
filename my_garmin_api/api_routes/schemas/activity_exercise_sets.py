"""Activity exercise sets schema models."""

from typing import Optional

from pydantic import BaseModel, Field


class ExerciseSetExerciseSchema(BaseModel):
    """Detected or planned exercise metadata for an exercise set."""

    category: Optional[str] = Field(
        default=None,
        title="Exercise Category",
        description="Exercise category key reported by Garmin.",
    )

    name: Optional[str] = Field(
        default=None,
        title="Exercise Name",
        description="Exercise name key reported by Garmin.",
    )

    probability: Optional[float] = Field(
        default=None,
        title="Exercise Match Probability",
        description="Confidence score for the detected exercise.",
    )


class ExerciseSetEntrySchema(BaseModel):
    """A single work/rest set entry in the Garmin exercise set timeline."""

    exercises: Optional[list[ExerciseSetExerciseSchema]] = Field(
        default=None,
        title="Exercises",
        description="List of exercises attached to this set entry.",
    )

    duration: Optional[float] = Field(
        default=None,
        title="Duration",
        description="Set duration in seconds.",
    )

    repetitionCount: Optional[int] = Field(
        default=None,
        title="Repetition Count",
        description="Number of repetitions recorded for this set.",
    )

    weight: Optional[float] = Field(
        default=None,
        title="Weight",
        description="Set weight/load value if available.",
    )

    setType: Optional[str] = Field(
        default=None,
        title="Set Type",
        description="Set classification such as ACTIVE or REST.",
    )

    startTime: Optional[str] = Field(
        default=None,
        title="Set Start Time",
        description="Set start timestamp in local time, ISO 8601 format.",
    )

    wktStepIndex: Optional[int] = Field(
        default=None,
        title="Workout Step Index",
        description="Workout step index for this set entry.",
    )

    messageIndex: Optional[int] = Field(
        default=None,
        title="Message Index",
        description="Message index for this set entry in Garmin payload order.",
    )


class ActivityExerciseSetsSchema(BaseModel):
    """Exercise set payload associated with an activity."""

    activityId: Optional[int] = Field(
        default=None,
        title="Activity ID",
        description="Unique Garmin activity identifier for this exercise set payload.",
    )

    exerciseSets: Optional[list[ExerciseSetEntrySchema]] = Field(
        default=None,
        title="Exercise Sets",
        description="Ordered list of exercise set entries for the activity.",
    )
