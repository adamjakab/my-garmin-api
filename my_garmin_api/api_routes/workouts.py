"""Workout endpoints for the FastAPI application."""

from datetime import date

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

import my_garmin_api.garmin_fit as gfit


router = APIRouter(tags=["activities"])


def _build_workout_response(workout_date: date, workouts: list[dict]) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={
            "date": workout_date.isoformat(),
            "count": len(workouts),
            "workouts": workouts,
        },
    )


@router.get("/workouts")
async def get_workouts(
    date_param: str = Query(
        default=None,
        description="Workout date in YYYY-MM-DD format. If omitted, uses today.",
        alias="date",
    ),
    tmp_dir: str = Query(
        default="tmp",
        description="Cache directory for workouts (default: tmp)",
    ),
    cache_ttl_seconds: int = Query(
        default=3600,
        description="Cache TTL in seconds (default: 3600 = 1 hour)",
    ),
) -> JSONResponse:
    """
    Fetch all available Garmin workout data for a specified date.

    Returns a JSON array of activities, each enriched with:
    - activity: activity summary (HR, calories, distance)
    - details: detailed activity chart, splits, lap data
    - splits, typed_splits, split_summaries: workout segmentation
    - weather: conditions at activity time/location
    - hr_time_in_zones, power_time_in_zones: zone distributions
    - exercise_sets, gear: exercise details, equipment used
    - errors: per-resource errors if any endpoint fails (graceful degradation)

    **Cache Behavior:**
    - Results are cached in `<tmp_dir>/workouts_YYYY-MM-DD.json`
    - Successive requests for the same date return cached data
    - If cache is older than `cache_ttl_seconds`, fresh data is fetched
    """
    try:
        workout_date = date.fromisoformat(date_param) if date_param else date.today()
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail="Date must use YYYY-MM-DD format",
        ) from exc

    try:
        workouts = gfit.get_workouts_for_date(
            workout_date=workout_date,
            tmp_dir=tmp_dir,
            cache_ttl_seconds=cache_ttl_seconds,
        )
        return _build_workout_response(workout_date, workouts)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch workouts: {str(exc)}",
        ) from exc


@router.get("/workouts/{date_str}")
async def get_workouts_by_date(
    date_str: str,
    tmp_dir: str = Query(
        default="tmp",
        description="Cache directory for workouts (default: tmp)",
    ),
    cache_ttl_seconds: int = Query(
        default=3600,
        description="Cache TTL in seconds (default: 3600 = 1 hour)",
    ),
) -> JSONResponse:
    """
    Fetch workouts for a specific date using path parameter.

    This is an alternative to the query parameter endpoint (`/workouts?date=YYYY-MM-DD`).

    **Parameters:**
    - `date_str`: Workout date in YYYY-MM-DD format (required, in path)
    - `tmp_dir`: Cache directory (optional query param)
    - `cache_ttl_seconds`: Cache TTL in seconds (optional query param)
    """
    try:
        workout_date = date.fromisoformat(date_str)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid date format: {date_str}. Use YYYY-MM-DD format",
        ) from exc

    try:
        workouts = gfit.get_workouts_for_date(
            workout_date=workout_date,
            tmp_dir=tmp_dir,
            cache_ttl_seconds=cache_ttl_seconds,
        )
        return _build_workout_response(workout_date, workouts)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch workouts for {date_str}: {str(exc)}",
        ) from exc