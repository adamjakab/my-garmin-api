"""HRV response schema models for FastAPI routes."""

from typing import Any

from pydantic import BaseModel, Field


class HrvEntrySchema(BaseModel):
    date: str = Field(
        title="Date",
        description="The date of the HRV payload in YYYY-MM-DD format.",
    )
    hrv: dict[str, Any] = Field(
        title="HRV Data",
        description="Raw Garmin HRV payload for the date.",
    )


class HrvResponseSchema(BaseModel):
    from_date: str = Field(
        title="Requester from date",
        description="The start date of the requested range in YYYY-MM-DD format.",
    )
    to_date: str = Field(
        title="Requester to date",
        description="The end date of the requested range in YYYY-MM-DD format.",
    )
    count: int = Field(
        title="Count",
        description="The number of HRV records returned for the selected date range.",
    )
    hrv_data: list[HrvEntrySchema]
