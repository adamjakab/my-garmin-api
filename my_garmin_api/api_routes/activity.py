"""Activity detail endpoint for the FastAPI application."""

from fastapi import APIRouter, HTTPException, Path

from my_garmin_api.api_routes.schemas.activities import ActivitySchema
import my_garmin_api.garmin_fit as gfit


router = APIRouter(tags=["Activity"])


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
) -> ActivitySchema:
    """
    Fetch full details for a specific activity.

    **Parameters:**
    - `activity_id`: The activity ID (positive integer, required)
    """
    try:
        activity = gfit.get_activity_by_id(activity_id)
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
