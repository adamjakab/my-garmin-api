"""Weight response schema models for FastAPI routes."""

from typing import Any

from pydantic import BaseModel, Field


class WeightEntrySchema(BaseModel):
    date: str = Field(
        title="Date",
        description="The measurement date in YYYY-MM-DD format.",
    )
    weight: dict[str, Any] = Field(
        title="Weight Data",
        description="Structured Garmin weight/body composition measurement payload for the date.",
    )


class WeightResponseSchema(BaseModel):
    start_date: str = Field(
        title="Requested start date",
        description="The start date of the requested range.",
    )
    end_date: str = Field(
        title="Requested end date",
        description="The end date of the requested range.",
    )
    count: int = Field(
        title="Count",
        description="The number of weight measurements returned for the selected date range.",
    )
    weight_data: list[WeightEntrySchema]
