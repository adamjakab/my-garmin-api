"""Activity endpoint for the FastAPI application."""

from datetime import date
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

import my_garmin_api.garmin_fit as gfit


class ActivityTypeSchema(BaseModel):
    typeId: int = Field(
        title="Type ID",
        description="The numeric identifier for the activity type.",
    )
    typeKey: str = Field(
        title="Type Key",
        description="The string key identifying the activity type (e.g., 'running', 'cycling').",
    )


class ActivitySummarySchema(BaseModel):
    activityName: str = Field(
        title="Activity Name",
        description="The name of the activity as set by the user or device.",
    )
    startTimeLocal: str = Field(
        title="Start Time Local",
        description="The activity start time in the local timezone of the device, in ISO 8601 format.",
    )
    startTimeGMT: str = Field(
        title="Start Time GMT",
        description="The activity start time in GMT/UTC, in ISO 8601 format.",
    )
    activityType: ActivityTypeSchema


class ActivitySchema(BaseModel):
    activity_id: int | None = None
    summary: ActivitySummarySchema
    errors: dict[str, str] | None = None


class ActivitiesResponseSchema(BaseModel):
    start_date: str = Field(
        title="Start Date",
        description="The start date of the requested range in YYYY-MM-DD format.",
    )
    end_date: str = Field(
        title="End Date",
        description="The end date of the requested range in YYYY-MM-DD format.",
    )
    count: int = Field(
        title="Count",
        description="The number of activities returned in the response for the selected date range.",
    )
    activities: list[ActivitySchema]


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
    description="Fetch all activity data for a date range between the specified start and end dates. This endpoint can be used to fetch activities for a single date (start_date same as end_date) or to get activities between two specific dates.",
    operation_id="getActivitiesByDateRange",
    response_model=ActivitiesResponseSchema,
    
)
async def get_activities(
    start_date: date = Query(
        description="Start date in YYYY-MM-DD format. This is a required parameter.",
    ),
    end_date: date= Query(
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
            detail=(
                "Failed to fetch activities for "
                f"{start_date.isoformat()} to {end_date.isoformat()}: {str(exc)}"
            ),
        ) from exc
