"""Activity endpoint for the FastAPI application."""

from datetime import date

from fastapi import APIRouter, HTTPException, Query

import my_garmin_api.garmin_fit as gfit
from my_garmin_api.api_routes.schemas.activities import ActivitySchema, ActivitiesResponseSchema


router = APIRouter(tags=["Activities"])


def _build_activity_response(
    start_date: date,
    end_date: date,
    activities: list[dict],
) -> ActivitiesResponseSchema:
    return ActivitiesResponseSchema(
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        count=len(activities),
        activities=[ActivitySchema.model_validate(a) for a in activities],
    )


@router.get(
    "/activities",
    summary="Fetch activities between two specific dates.",
    description=(
        "Fetch all activity data for a date range between the specified start and end dates. "
        "This endpoint can be used to fetch activities for a single date (start_date same as "
        "end_date) or to get activities between two specific dates."
    ),
    operation_id="getActivitiesByDateRange",
    response_model=ActivitiesResponseSchema,
)
async def get_activities(
    start_date: date = Query(
        description="Start date in YYYY-MM-DD format. This is a required parameter.",
    ),
    end_date: date = Query(
        description="End date in YYYY-MM-DD format. This is a required parameter.",
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
        return _build_activity_response(
            start_date,
            end_date,
            activities,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(f"Failed to fetch activities for {start_date.isoformat()} to {end_date.isoformat()}: {str(exc)}"),
        ) from exc
