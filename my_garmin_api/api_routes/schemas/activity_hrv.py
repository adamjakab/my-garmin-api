"""HRV response schema models for FastAPI routes."""

from typing import Any

from pydantic import BaseModel, Field


class HrvResponseSchema(BaseModel):
    date: str = Field(
        title="Requested date",
        description="The requested date in YYYY-MM-DD format.",
    )
    hrv: dict[str, Any] = Field(
        title="HRV Data",
        description="Raw Garmin HRV payload for the requested date.",
    )
