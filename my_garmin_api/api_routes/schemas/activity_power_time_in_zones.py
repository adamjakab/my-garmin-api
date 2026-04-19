"""Power time-in-zones schema models."""

from typing import Optional

from pydantic import BaseModel, Field


class PowerTimeInZoneSchema(BaseModel):
    """Time spent in a power zone during an activity."""

    zoneNumber: Optional[int] = Field(
        default=None,
        title="Zone Number",
        description="Power zone index (typically 1-5).",
    )

    secsInZone: Optional[float] = Field(
        default=None,
        title="Seconds In Zone",
        description="Total time spent in the zone, in seconds.",
    )

    zoneLowBoundary: Optional[int] = Field(
        default=None,
        title="Zone Low Boundary",
        description="Lower power boundary for the zone, in watts.",
    )
