"""Activities response schema models for FastAPI routes."""

from pydantic import BaseModel, Field

from my_garmin_api.api_routes.schemas.activity import ActivitySchema


class ActivitiesResponseSchema(BaseModel):
    start_date: str = Field(
        title="Requester start date",
        description="The start date of the requested range in YYYY-MM-DD format.",
    )

    end_date: str = Field(
        title="Requester end date",
        description="The end date of the requested range in YYYY-MM-DD format.",
    )

    count: int = Field(
        title="Count",
        description="The number of activities returned in the response for the selected date range.",
    )

    # The list of activities
    activities: list[ActivitySchema]
