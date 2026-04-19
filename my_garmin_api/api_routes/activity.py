"""Activity detail endpoint for the FastAPI application."""

from fastapi import APIRouter, HTTPException, Path, Query

from my_garmin_api.api_routes.schemas.activity import ActivitySchema
from my_garmin_api.helpers.activity_enrichment import ActivityResourceName
import my_garmin_api.garmin_fit as gfit


router = APIRouter(tags=["Activity"])

_YN_DESC = 'Include this enrichment block. Use "Y" to include or "N" to exclude.'


@router.get(
    "/activity/{activity_id}",
    summary="Fetch activity details by ID.",
    description="Fetch full details for a specific activity by its ID.",
    operation_id="getActivityById",
    response_model=ActivitySchema,
)
async def get_activity(
    activity_id: str = Path(
        ...,
        title="Activity ID",
        description="The unique identifier of the Garmin activity.",
    ),
    details: str = Query(default="Y", description=_YN_DESC, pattern="^[YyNn]$"),
    splits: str = Query(default="Y", description=_YN_DESC, pattern="^[YyNn]$"),
    typed_splits: str = Query(default="Y", description=_YN_DESC, pattern="^[YyNn]$"),
    split_summaries: str = Query(default="Y", description=_YN_DESC, pattern="^[YyNn]$"),
    exercise_sets: str = Query(default="Y", description=_YN_DESC, pattern="^[YyNn]$"),
    hr_time_in_zones: str = Query(default="Y", description=_YN_DESC, pattern="^[YyNn]$"),
    power_time_in_zones: str = Query(default="Y", description=_YN_DESC, pattern="^[YyNn]$"),
    weather: str = Query(default="Y", description=_YN_DESC, pattern="^[YyNn]$"),
    gear: str = Query(default="Y", description=_YN_DESC, pattern="^[YyNn]$"),
) -> ActivitySchema:
    """
    Fetch full details for a specific activity.

    **Parameters:**
    - `activity_id`: The activity ID (positive integer, required)
    - `details`, `splits`, `typed_splits`, `split_summaries`, `exercise_sets`,
      `hr_time_in_zones`, `power_time_in_zones`, `weather`, `gear`:
      Y/N flags controlling which enrichment blocks are included (default: Y).
    """
    enabled: set[ActivityResourceName] = {
        resource  # type: ignore[misc]
        for resource, flag in [
            ("details", details),
            ("splits", splits),
            ("typed_splits", typed_splits),
            ("split_summaries", split_summaries),
            ("exercise_sets", exercise_sets),
            ("hr_time_in_zones", hr_time_in_zones),
            ("power_time_in_zones", power_time_in_zones),
            ("weather", weather),
            ("gear", gear),
        ]
        if flag.upper() == "Y"
    }
    try:
        activity = gfit.get_activity_by_id(activity_id, enabled_enrichments=enabled)
        if activity is None:
            raise HTTPException(
                status_code=404,
                detail=f"Activity with ID {activity_id} not found.",
            )
        return ActivitySchema.model_validate(activity)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch activity {activity_id}: {str(exc)}",
        ) from exc
