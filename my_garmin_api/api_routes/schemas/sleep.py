"""Sleep response schema models for FastAPI routes."""

from typing import Optional

from pydantic import BaseModel, Field


class SleepMetricsSchema(BaseModel):
    score: Optional[int] = Field(
        default=None,
        title="Sleep Score",
        description="Garmin sleep score for the night.",
    )
    duration_seconds: Optional[int] = Field(
        default=None,
        title="Sleep Duration (Seconds)",
        description="Total sleep duration in seconds.",
    )


class SleepEntrySchema(BaseModel):
    date: str = Field(
        title="Date",
        description="The date of the sleep payload in YYYY-MM-DD format.",
    )
    sleep: SleepMetricsSchema = Field(
        title="Sleep Data",
        description="Sleep score and duration for the date.",
    )


class SleepResponseSchema(BaseModel):
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
        description="The number of sleep records returned for the selected date range.",
    )
    sleep_data: list[SleepEntrySchema]
