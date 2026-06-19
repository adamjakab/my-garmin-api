"""VO2 max response schema models for FastAPI routes."""

from pydantic import BaseModel, Field


class Vo2MaxEntrySchema(BaseModel):
    date: str = Field(
        title="Date",
        description="The date of the VO2 max payload in YYYY-MM-DD format.",
    )
    vo2max_precise_value: float = Field(
        title="VO2 Max Precise Value",
        description="Highest Garmin vo2MaxPreciseValue available for the date.",
    )


class Vo2MaxResponseSchema(BaseModel):
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
        description="The number of VO2 max records returned for the selected date range.",
    )
    vo2max_data: list[Vo2MaxEntrySchema]
