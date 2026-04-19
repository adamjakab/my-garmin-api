"""Heart rate time-in-zones schema models."""

from typing import Optional

from pydantic import BaseModel, Field


class HrTimeInZoneSchema(BaseModel):
    zoneNumber: Optional[int] = Field(
        default=None,
        title="Zone Number",
        description="Heart rate zone index (typically 1-5).",
    )

    secsInZone: Optional[float] = Field(
        default=None,
        title="Seconds In Zone",
        description="Total time spent in the zone, in seconds.",
    )

    zoneLowBoundary: Optional[int] = Field(
        default=None,
        title="Zone Low Boundary",
        description="Lower heart rate boundary for the zone, in BPM.",
    )
