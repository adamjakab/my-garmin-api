"""HRV endpoint for the FastAPI application."""

from datetime import date

from fastapi import APIRouter, HTTPException, Query

from my_garmin_api.api_routes.schemas.hrv import HrvResponseSchema
import my_garmin_api.garmin_fit as gfit


router = APIRouter(tags=["HRV"])


@router.get(
    "/hrv",
    summary="Fetch HRV data for a date or date range.",
    description=(
        "Fetch heart-rate variability (HRV) data for a date range between the specified start and end dates. "
        "This endpoint can be used to fetch HRV data for a single date (start_date same as "
        "end_date) or to get HRV data between two specific dates."
    ),
    operation_id="getHrvByDateRange",
    response_model=HrvResponseSchema,
)
async def get_hrv(
    start_date: date = Query(
        description="Start date of the HRV data request in YYYY-MM-DD format.",
    ),
    end_date: date = Query(
        description="End date of the HRV data request in YYYY-MM-DD format.",
    ),
) -> HrvResponseSchema:
    """Fetch HRV data for an inclusive date range."""
    resolved_end_date = end_date or start_date
    if resolved_end_date < start_date:
        raise HTTPException(
            status_code=400,
            detail="end_date cannot be before start_date",
        )

    try:
        hrv_payload = gfit.get_hrv_for_date_range(from_date=start_date, to_date=resolved_end_date)
        if hrv_payload is None or hrv_payload.get("count", 0) == 0:
            raise HTTPException(
                status_code=404,
                detail=f"No HRV data found for {start_date.isoformat()} to {resolved_end_date.isoformat()}",
            )

        return HrvResponseSchema.model_validate(hrv_payload)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch HRV for {start_date.isoformat()} to {resolved_end_date.isoformat()}: {str(exc)}",
        ) from exc
