"""RHR endpoint for the FastAPI application."""

from datetime import date

from fastapi import APIRouter, HTTPException, Query

from my_garmin_api.api_routes.schemas import RhrResponseSchema
import my_garmin_api.garmin_fit as gfit


router = APIRouter()


@router.get(
    "/rhr",
    summary="Get resting heart rate data",
    description=(
        "Fetch resting heart rate (RHR) data from Garmin. "
        "Fetch RHR data for a single date (start_date same as end_date) or "
        "for a date range between the start and end dates. "
    ),
    tags=["Health"],
    operation_id="getRhrByDateRange",
    response_model=RhrResponseSchema,
)
async def get_rhr(
    start_date: date = Query(
        description="This required parameter is the start of the requested date range. Format: YYYY-MM-DD ",
    ),
    end_date: date = Query(
        description="This required parameter is the end of the requested date range. Format: YYYY-MM-DD ",
    ),
) -> RhrResponseSchema:
    """Fetch resting heart rate data for an inclusive date range."""
    if end_date < start_date:
        raise HTTPException(
            status_code=400,
            detail="end_date cannot be before start_date",
        )

    try:
        rhr_payload = gfit.get_rhr_for_date_range(from_date=start_date, to_date=end_date)
        if rhr_payload is None or rhr_payload.get("count", 0) == 0:
            raise HTTPException(
                status_code=404,
                detail=f"No resting heart rate data found for {start_date.isoformat()} to {end_date.isoformat()}",
            )

        return RhrResponseSchema.model_validate(rhr_payload)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Failed to fetch resting heart rate for {start_date.isoformat()} to {end_date.isoformat()}: {str(exc)}"
            ),
        ) from exc
