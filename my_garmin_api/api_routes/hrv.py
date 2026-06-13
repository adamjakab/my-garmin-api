"""HRV endpoint for the FastAPI application."""

from datetime import date

from fastapi import APIRouter, HTTPException, Query

from my_garmin_api.api_routes.schemas.activity_hrv import HrvResponseSchema
import my_garmin_api.garmin_fit as gfit


router = APIRouter(tags=["HRV"])


@router.get(
    "/hrv",
    summary="Fetch HRV data for a specific date.",
    description=(
        "Fetch heart-rate variability (HRV) data from Garmin Connect for a specific date. "
        "The date must be provided in YYYY-MM-DD format."
    ),
    operation_id="getHrvByDate",
    response_model=HrvResponseSchema,
)
async def get_hrv_by_date(
    hrv_date: date = Query(
        ...,
        alias="date",
        description="Date of the HRV data to fetch in YYYY-MM-DD format.",
    ),
) -> HrvResponseSchema:
    """Fetch HRV data for a specific date."""
    try:
        hrv_payload = gfit.get_hrv_for_date(hrv_date)
        if hrv_payload is None:
            raise HTTPException(
                status_code=404,
                detail=f"No HRV data found for {hrv_date.isoformat()}",
            )

        return HrvResponseSchema.model_validate(hrv_payload)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch HRV for {hrv_date.isoformat()}: {str(exc)}",
        ) from exc
