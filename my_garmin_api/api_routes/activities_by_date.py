"""Activity endpoint for the FastAPI application."""

from datetime import date

from fastapi import APIRouter, HTTPException, Query

import my_garmin_api.garmin_fit as gfit
from my_garmin_api.api_routes.schemas.activities import ActivitiesResponseSchema


router = APIRouter(tags=["Activities"])


@router.get(
    "/activities",
    name="Get Activities",
    summary="Fetch run or other activity data between two specific dates.",
    description=(
        "Fetch a list of physical activities from Garmin for a date range. "
        "Fetch activities for a single date (start_date same as end_date) or between the start and end dates. "
    ),
    tags=["Garmin", "Activity"],
    operation_id="getActivitiesByDateRange",
    response_model=ActivitiesResponseSchema,
)
async def get_activities(
    start_date: date = Query(
        description=(
            "This parameter controls the start of the requested activity date range. "
            "Provide it in YYYY-MM-DD format. This is a required parameter."
        ),
    ),
    end_date: date = Query(
        description=(
            "This parameter controls the end of the requested activity date range. "
            "Provide it in YYYY-MM-DD format. This is a required parameter."
        ),
    ),
) -> ActivitiesResponseSchema:
    """
    Fetch activities for an inclusive date range.

    **Parameters:**
    - `start_date`: Range start in YYYY-MM-DD format (required)
    - `end_date`: Range end in YYYY-MM-DD format (required)
    """
    if end_date < start_date:
        raise HTTPException(
            status_code=400,
            detail="end_date cannot be before start_date",
        )

    try:
        activities = gfit.get_activities_for_date_range(
            start_date=start_date,
            end_date=end_date,
        )
        if activities is None:
            return ActivitiesResponseSchema(
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
                count=0,
                activities=[],
            )

        return ActivitiesResponseSchema.model_validate(activities)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(f"Failed to fetch activities for {start_date.isoformat()} to {end_date.isoformat()}: {str(exc)}"),
        ) from exc
