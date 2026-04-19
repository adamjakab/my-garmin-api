"""Activity detail endpoint for the FastAPI application."""

from fastapi import APIRouter, HTTPException, Path, Query

from my_garmin_api.api_routes.schemas.activity import ActivitySchema
from my_garmin_api.helpers.activity_enrichment import ActivityResourceName
import my_garmin_api.garmin_fit as gfit


router = APIRouter(tags=["Activity"])

_YN_DESC = 'Use "Y" to include this enrichment block.'


@router.get(
    "/activity/{activity_id}",
    summary="Fetch detailed activity information.",
    description=(
        "Fetch full details for a specific activity by ID. "
        "Use query parameters to select enrichment blocks for the response. "
        "Returns a comprehensive activity view with summary metrics and optional details, splits, laps, "
        "exercise sets, time in zones, weather, and gear."
    ),
    operation_id="getActivityById",
    response_model=ActivitySchema,
)
async def get_activity(
    activity_id: str = Path(
        ...,
        title="Activity ID",
        description="The unique identifier of the Garmin activity.",
    ),
    details: str = Query(
        default="N",
        description=(
            "This flag controls whether to include the detailed metrics about the activity aggregated for each 60 second interval. "
            "Each metric (heart rate, speed, cadence, etc.) includes time in zone buckets with min/max/avg values. "
            "" + _YN_DESC
        ),
        pattern="^[YyNn]$",
    ),
    splits: str = Query(
        default="N",
        description=(
            "This flag controls whether to include auto-generated lap information and events. "
            "Laps are typically emitted at regular distance intervals (e.g. every 1 km during runs) and include aggregated metrics for that lap. "
            "Events include automatic notifications emitted during the activity, such as warnings for heart rate or pace being outside of the planned range. "
            "" + _YN_DESC
        ),
        pattern="^[YyNn]$",
    ),
    typed_splits: str = Query(
        default="N",
        description=(
            "This flag controls whether to include workout-phase splits such as active and rest intervals with per-phase metrics. "
            "Typed splits group split data by Garmin split type (active, rest, etc.) for easier comparison. "
            "" + _YN_DESC
        ),
        pattern="^[YyNn]$",
    ),
    split_summaries: str = Query(
        default="N",
        description=(
            "This flag controls whether to include summary information for splits. "
            "Split summaries provide aggregate stats over all splits, helping you quickly assess consistency and pacing. "
            "" + _YN_DESC
        ),
        pattern="^[YyNn]$",
    ),
    exercise_sets: str = Query(
        default="N",
        description=(
            "This flag controls whether to include exercise set information. "
            "Exercise sets include structured workout steps and set-level performance information when present. "
            "" + _YN_DESC
        ),
        pattern="^[YyNn]$",
    ),
    hr_time_in_zones: str = Query(
        default="N",
        description=(
            "This flag controls whether to include heart rate time in zones information. "
            "Heart rate time in zones reports cumulative time spent in each configured heart rate zone. "
            "" + _YN_DESC
        ),
        pattern="^[YyNn]$",
    ),
    power_time_in_zones: str = Query(
        default="N",
        description=(
            "This flag controls whether to include power time in zones information. "
            "Power time in zones reports cumulative time spent in each configured cycling power zone. "
            "" + _YN_DESC
        ),
        pattern="^[YyNn]$",
    ),
    weather: str = Query(
        default="N",
        description=(
            "This flag controls whether to include weather information. "
            "Weather includes environmental conditions recorded for the activity such as temperature, humidity, and wind. "
            "" + _YN_DESC
        ),
        pattern="^[YyNn]$",
    ),
    gear: str = Query(
        default="N",
        description=(
            "This flag controls whether to include gear information. "
            "Gear includes equipment associated with the activity, such as shoes or bike components when available. "
            "" + _YN_DESC
        ),
        pattern="^[YyNn]$",
    ),
) -> ActivitySchema:
    """
    Fetch full details for a specific activity.

    **Parameters:**
    - `activity_id`: The activity ID (positive integer, required)
    - `details`, `splits`, `typed_splits`, `split_summaries`, `exercise_sets`,
      `hr_time_in_zones`, `power_time_in_zones`, `weather`, `gear`:
            Y/N flags controlling which enrichment blocks are included (default: N).
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
