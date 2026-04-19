"""Activity schema models for FastAPI routes."""

from typing import Any

from pydantic import BaseModel, Field

from my_garmin_api.api_routes.schemas.activity_details import AggregatedDetailsSchema
from my_garmin_api.api_routes.schemas.activity_summary import ActivitySummarySchema


class ActivitySchema(BaseModel):
    activity_id: int | None = None

    summary: ActivitySummarySchema

    details: AggregatedDetailsSchema | None = Field(
        default=None,
        title="Activity Details",
        description="Aggregated activity detail metrics with time-bucketed statistics.",
    )

    # TODO: This needs a proper schema definition!
    splits: dict[str, Any] | None = Field(
        default=None,
        title="Activity Splits",
        description="List of activity splits with their respective metrics.",
    )

    # TODO: This needs a proper schema definition!
    typed_splits: dict[str, Any] | None = Field(
        default=None,
        title="Typed Activity Splits",
        description="List of typed activity splits with their respective metrics.",
    )

    # TODO: This needs a proper schema definition!
    split_summaries: dict[str, Any] | None = Field(
        default=None,
        title="Split Summaries",
        description="List of split summaries with their respective metrics.",
    )

    # TODO: This needs a proper schema definition!
    exercise_sets: dict[str, Any] | None = Field(
        default=None,
        title="Exercise Sets",
        description="Exercise sets information associated with the activity.",
    )

    # TODO: This needs a proper schema definition!
    hr_time_in_zones: list[dict[str, Any]] | None = Field(
        default=None,
        title="HR Time In Zones",
        description="Time spent in each heart rate zone during the activity.",
    )

    # TODO: This needs a proper schema definition!
    power_time_in_zones: list[dict[str, Any]] | None = Field(
        default=None,
        title="Power Time In Zones",
        description="Time spent in each power zone during the activity.",
    )

    # TODO: This needs a proper schema definition!
    weather: dict[str, Any] | None = Field(
        default=None,
        title="Weather",
        description="Weather information associated with the activity.",
    )

    # TODO: This needs a proper schema definition!
    gear: list[dict[str, Any]] | None = Field(
        default=None,
        title="Gear",
        description="List of gear associated with the activity.",
    )

    errors: dict[str, str] | None = None
