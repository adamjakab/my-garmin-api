"""Activity schema models for FastAPI routes."""

from typing import Any, Optional

from pydantic import BaseModel, Field

from .activity_details import AggregatedDetailsSchema
from .activity_exercise_sets import ActivityExerciseSetsSchema
from .activity_hr_time_in_zones import HrTimeInZoneSchema
from .activity_split_summaries import ActivitySplitSummariesSchema
from .activity_splits import ActivitySplitsSchema
from .activity_summary import ActivitySummarySchema
from .activity_typed_splits import ActivityTypedSplitsSchema


class ActivitySchema(BaseModel):
    activity_id: Optional[int] = None

    summary: ActivitySummarySchema

    details: Optional[AggregatedDetailsSchema] = Field(
        default=None,
        title="Activity Details",
        description="Aggregated activity detail metrics with time-bucketed statistics.",
    )

    splits: Optional[ActivitySplitsSchema] = Field(
        default=None,
        title="Activity Splits",
        description="Structured activity split payload including lap and event details.",
    )

    typed_splits: Optional[ActivityTypedSplitsSchema] = Field(
        default=None,
        title="Typed Activity Splits",
        description="Structured workout-phase splits with active/rest interval metrics.",
    )

    split_summaries: Optional[ActivitySplitSummariesSchema] = Field(
        default=None,
        title="Split Summaries",
        description="List of split summaries with their respective metrics.",
    )

    exercise_sets: Optional[ActivityExerciseSetsSchema] = Field(
        default=None,
        title="Exercise Sets",
        description="Exercise sets information associated with the activity.",
    )

    hr_time_in_zones: Optional[list[HrTimeInZoneSchema]] = Field(
        default=None,
        title="HR Time In Zones",
        description="Time spent in each heart rate zone during the activity.",
    )

    # TODO: This needs a proper schema definition!
    power_time_in_zones: Optional[list[dict[str, Any]]] = Field(
        default=None,
        title="Power Time In Zones",
        description="Time spent in each power zone during the activity.",
    )

    # TODO: This needs a proper schema definition!
    weather: Optional[dict[str, Any]] = Field(
        default=None,
        title="Weather",
        description="Weather information associated with the activity.",
    )

    # TODO: This needs a proper schema definition!
    gear: Optional[list[dict[str, Any]]] = Field(
        default=None,
        title="Gear",
        description="List of gear associated with the activity.",
    )

    errors: Optional[dict[str, str]] = None
