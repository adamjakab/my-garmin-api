"""VO2 max endpoint for the FastAPI application."""

from datetime import date

from fastapi import APIRouter, HTTPException, Query

from my_garmin_api.api_routes.schemas import Vo2MaxResponseSchema
from my_garmin_api.garmin_fit import get_vo2max_for_date_range


router = APIRouter()


@router.get(
    "/vo2max",
    summary="Get VO2 max data",
    description=(
        "Fetch VO2 max data from Garmin. "
        "Fetch VO2 max data for a single date (start_date same as end_date) or "
        "for a date range between the start and end dates. "
    ),
    tags=["Health"],
    operation_id="getVo2MaxByDateRange",
    response_model=Vo2MaxResponseSchema,
)
async def get_vo2max(
    start_date: date = Query(
        description="This required parameter is the start of the requested date range. Format: YYYY-MM-DD ",
    ),
    end_date: date = Query(
        description="This required parameter is the end of the requested date range. Format: YYYY-MM-DD ",
    ),
) -> Vo2MaxResponseSchema:
    """Fetch VO2 max data for an inclusive date range."""
    if end_date < start_date:
        raise HTTPException(
            status_code=400,
            detail="end_date cannot be before start_date",
        )

    try:
        vo2max_payload = get_vo2max_for_date_range(from_date=start_date, to_date=end_date)
        if vo2max_payload is None or vo2max_payload.get("count", 0) == 0:
            raise HTTPException(
                status_code=404,
                detail=f"No VO2 max data found for {start_date.isoformat()} to {end_date.isoformat()}",
            )

        return Vo2MaxResponseSchema.model_validate(vo2max_payload)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch VO2 max for {start_date.isoformat()} to {end_date.isoformat()}: {str(exc)}",
        ) from exc
