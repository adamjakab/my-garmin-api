"""Activity endpoint for the FastAPI application."""

from datetime import date

from fastapi import APIRouter, HTTPException, Query

import my_garmin_api.garmin_fit as gfit
from my_garmin_api.api_routes.schemas.activities import ActivitiesResponseSchema


router = APIRouter()


@router.get(
    "/activities",
    summary="Get Garmin activities",
    description=(
        "Fetch a list of physical activities from Garmin. "
        "Fetch activities for a single date (start_date same as end_date) or "
        "for a date range between the start and end dates. "
    ),
    tags=["Activity"],
    operation_id="getActivitiesByDateRange",
    response_model=ActivitiesResponseSchema,
)
async def get_activities(
    start_date: date = Query(
        description=("This required parameter is the start of the requested date range. Format: YYYY-MM-DD "),
    ),
    end_date: date = Query(
        description=("This required parameter is the end of the requested date range. Format: YYYY-MM-DD "),
    ),
) -> ActivitiesResponseSchema:
    """
    Fetch activities for an inclusive date range.
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
