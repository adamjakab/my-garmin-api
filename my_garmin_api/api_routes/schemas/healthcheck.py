"""Health endpoint schema models."""

from pydantic import BaseModel, Field


class HealthResponseSchema(BaseModel):
    """Structured health payload used by the root health endpoint."""

    status: str = Field(
        title="Status",
        description="Health status indicator for the service.",
        examples=["ok"],
    )
    message: str = Field(
        title="Message",
        description="Human-readable service health message.",
        examples=["My Garmin API is running"],
    )
    version: str = Field(
        title="Version",
        description="Service version resolved from project metadata.",
        examples=["0.1.0"],
    )
