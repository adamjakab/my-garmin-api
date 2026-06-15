"""Sleep endpoint for the FastAPI application."""

from datetime import date

from fastapi import APIRouter, HTTPException, Query

from my_garmin_api.api_routes.schemas.sleep import SleepResponseSchema
from my_garmin_api.garmin_fit import get_sleep_for_date_range


router = APIRouter()


@router.get(
    "/sleep",
    summary="Get sleep score and duration data",
    description=(
        "Fetch Garmin sleep score and duration data. "
        "Fetch sleep data for a single date (start_date same as end_date) or "
        "for a date range between the start and end dates. "
    ),
    tags=["Health"],
    operation_id="getSleepByDateRange",
    response_model=SleepResponseSchema,
)
async def get_sleep(
    start_date: date = Query(
        description="This required parameter is the start of the requested date range. Format: YYYY-MM-DD ",
    ),
    end_date: date = Query(
        description="This required parameter is the end of the requested date range. Format: YYYY-MM-DD ",
    ),
) -> SleepResponseSchema:
    """Fetch Garmin sleep score and duration for an inclusive date range."""
    if end_date < start_date:
        raise HTTPException(
            status_code=400,
            detail="end_date cannot be before start_date",
        )

    try:
        sleep_payload = get_sleep_for_date_range(from_date=start_date, to_date=end_date)
        if sleep_payload is None or sleep_payload.get("count", 0) == 0:
            raise HTTPException(
                status_code=404,
                detail=f"No sleep data found for {start_date.isoformat()} to {end_date.isoformat()}",
            )

        return SleepResponseSchema.model_validate(sleep_payload)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch sleep data for {start_date.isoformat()} to {end_date.isoformat()}: {str(exc)}",
        ) from exc
