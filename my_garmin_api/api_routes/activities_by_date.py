"""Activity endpoint for the FastAPI application."""

from datetime import date
from typing import Any, Optional
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
    summary="Fetch activities for a date range",
    description="Fetch all available Garmin activity data for an inclusive date range between the specified start and end dates.",
    operation_id="getActivitiesByDateRange",
    response_model=ActivitiesResponseSchema,
)
async def get_activities(
    start_date: date = Query(
        description="Start date in YYYY-MM-DD format. This is a required parameter.",
    ),
    end_date: Optional[date] = Query(
        default=None,
        description="End date in YYYY-MM-DD format. If omitted, uses start_date.",
    ),
) -> ActivitiesResponseSchema:
    """
    Fetch activities for an inclusive date range.

    If `end_date` is omitted, it defaults to `start_date`.

    **Parameters:**
    - `start_date`: Range start in YYYY-MM-DD format (required)
    - `end_date`: Range end in YYYY-MM-DD format (optional, defaults to start_date)
    """
    parsed_end_date = end_date if end_date else start_date

    if parsed_end_date < start_date:
        raise HTTPException(
            status_code=400,
            detail="end_date cannot be before start_date",
        )

    try:
        activities = gfit.get_activities_for_date_range(
            start_date=start_date,
            end_date=parsed_end_date,
        )
        return _build_activity_response(
            start_date,
            parsed_end_date,
            activities,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to fetch activities for "
                f"{start_date.isoformat()} to {parsed_end_date.isoformat()}: {str(exc)}"
            ),
        ) from exc
