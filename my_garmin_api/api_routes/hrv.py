"""HRV endpoint for the FastAPI application."""

from datetime import date

from fastapi import APIRouter, HTTPException, Query

from my_garmin_api.api_routes.schemas.activity_hrv import HrvResponseSchema
import my_garmin_api.garmin_fit as gfit


router = APIRouter(tags=["HRV"])


@router.get(
    "/hrv",
    summary="Fetch HRV data for a date or date range.",
    description=(
        "Fetch heart-rate variability (HRV) data from Garmin Connect for an inclusive date range. "
        "Use `from_date` only to fetch a single day, or provide both `from_date` and `to_date`."
    ),
    operation_id="getHrvByDateRange",
    response_model=HrvResponseSchema,
)
async def get_hrv(
    from_date: date = Query(
        ...,
        description="Start date of the HRV data request in YYYY-MM-DD format.",
    ),
    to_date: date | None = Query(
        default=None,
        description="Optional end date of the HRV data request in YYYY-MM-DD format.",
    ),
) -> HrvResponseSchema:
    """Fetch HRV data for an inclusive date range."""
    resolved_to_date = to_date or from_date
    if resolved_to_date < from_date:
        raise HTTPException(
            status_code=400,
            detail="to_date cannot be before from_date",
        )

    try:
        hrv_payload = gfit.get_hrv_for_date_range(from_date=from_date, to_date=resolved_to_date)
        if hrv_payload is None or hrv_payload.get("count", 0) == 0:
            raise HTTPException(
                status_code=404,
                detail=f"No HRV data found for {from_date.isoformat()} to {resolved_to_date.isoformat()}",
            )

        return HrvResponseSchema.model_validate(hrv_payload)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch HRV for {from_date.isoformat()} to {resolved_to_date.isoformat()}: {str(exc)}",
        ) from exc
