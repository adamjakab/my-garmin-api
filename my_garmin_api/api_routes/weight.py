"""Weight endpoint for the FastAPI application."""

from datetime import date

from fastapi import APIRouter, HTTPException, Query

from my_garmin_api.api_routes.schemas.weight import WeightResponseSchema
from my_garmin_api.garmin_fit import get_weight_for_date_range


router = APIRouter()


@router.get(
    "/weight",
    summary="Get weight measurements",
    description=(
        "Fetch weight/body composition measurements from Garmin. "
        "Fetch data for a single date (start_date same as end_date) or "
        "for a date range between the start and end dates. "
    ),
    tags=["Health"],
    operation_id="getWeightByDateRange",
    response_model=WeightResponseSchema,
)
async def get_weight(
    start_date: date = Query(
        description="This required parameter is the start of the requested date range. Format: YYYY-MM-DD ",
    ),
    end_date: date = Query(
        description="This required parameter is the end of the requested date range. Format: YYYY-MM-DD ",
    ),
) -> WeightResponseSchema:
    """Fetch Garmin weight measurements for an inclusive date range."""
    if end_date < start_date:
        raise HTTPException(
            status_code=400,
            detail="end_date cannot be before start_date",
        )

    try:
        weight_payload = get_weight_for_date_range(from_date=start_date, to_date=end_date)
        if weight_payload is None or weight_payload.get("count", 0) == 0:
            raise HTTPException(
                status_code=404,
                detail=f"No weight data found for {start_date.isoformat()} to {end_date.isoformat()}",
            )

        return WeightResponseSchema.model_validate(weight_payload)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch weight for {start_date.isoformat()} to {end_date.isoformat()}: {str(exc)}",
        ) from exc
