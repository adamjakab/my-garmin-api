"""Activity endpoint for the FastAPI application."""

from datetime import date

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

import my_garmin_api.garmin_fit as gfit


router = APIRouter(tags=["Activities"])


def _build_activity_response(
    start_date: date,
    end_date: date,
    activities: list[dict],
) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "count": len(activities),
            "activities": activities,
        },
    )


@router.get("/activities",
            summary="Fetch activities for a date range",
            description="Fetch all available Garmin workout data for an inclusive date range."
            )
async def get_activities(
    start_date: str | None = Query(
        default=None,
        description="Start date in YYYY-MM-DD format. If omitted, uses today.",
    ),
    end_date: str | None = Query(
        default=None,
        description="End date in YYYY-MM-DD format. If omitted, uses start_date.",
    ),
) -> JSONResponse:
    """
    Fetch activities for an inclusive date range.

    If `start_date` is omitted, today's date is used.
    If `end_date` is omitted, it defaults to `start_date`.

    **Parameters:**
    - `start_date`: Range start in YYYY-MM-DD format (optional query param)
    - `end_date`: Range end in YYYY-MM-DD format (optional query param)
    """
    try:
        parsed_start_date = date.fromisoformat(start_date) if start_date else date.today()
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid start_date format. Use YYYY-MM-DD format",
        ) from exc

    try:
        parsed_end_date = (
            date.fromisoformat(end_date) if end_date else parsed_start_date
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid end_date format. Use YYYY-MM-DD format",
        ) from exc

    if parsed_end_date < parsed_start_date:
        raise HTTPException(
            status_code=400,
            detail="end_date cannot be before start_date",
        )

    try:
        activities = gfit.get_activities_for_date_range(
            start_date=parsed_start_date,
            end_date=parsed_end_date,
        )
        return _build_activity_response(
            parsed_start_date,
            parsed_end_date,
            activities,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to fetch activities for "
                f"{parsed_start_date.isoformat()} to {parsed_end_date.isoformat()}: {str(exc)}"
            ),
        ) from exc