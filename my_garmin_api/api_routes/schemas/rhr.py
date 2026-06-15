"""RHR response schema models for FastAPI routes."""

from typing import Any

from pydantic import BaseModel, Field


class RhrEntrySchema(BaseModel):
    date: str = Field(
        title="Date",
        description="The date of the resting heart rate payload in YYYY-MM-DD format.",
    )
    rhr: dict[str, Any] = Field(
        title="RHR Data",
        description="Structured Garmin resting heart rate payload for the date.",
    )


class RhrResponseSchema(BaseModel):
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
        description="The number of resting heart rate records returned for the selected date range.",
    )
    rhr_data: list[RhrEntrySchema]
