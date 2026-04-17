"""FastAPI application for exposing Garmin workout data via HTTP API with OpenAPI schema."""

import os
from datetime import date

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import uvicorn

import my_garmin_api.garmin_fit as gfit

load_dotenv()

app = FastAPI(
    title="My Garmin API",
    description="REST API for fetching and caching Garmin Connect workout data. "
    "Use the `/openapi.json` endpoint to retrieve the OpenAPI 3.0 schema for ChatGPT GPT integration.",
    version="0.1.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)


SERVER_MODES = {
    "development": {
        "host": "127.0.0.1",
        "port": 8000,
        "reload": True,
    },
    "production": {
        "host": "0.0.0.0",
        "port": 8000,
        "reload": False,
    },
}


@app.get("/", tags=["health"])
async def health_check() -> dict[str, str]:
    """Health check endpoint..."""
    return {"status": "ok", "message": "My Garmin API is running"}


@app.get("/workouts", tags=["activities"])
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
        if date_param:
            try:
                workout_date = date.fromisoformat(date_param)
            except ValueError as exc:
                raise HTTPException(
                    status_code=400,
                    detail="Date must use YYYY-MM-DD format",
                ) from exc
        else:
            workout_date = date.today()

        workouts = gfit.get_workouts_for_date(
            workout_date=workout_date,
            tmp_dir=tmp_dir,
            cache_ttl_seconds=cache_ttl_seconds,
        )

        return JSONResponse(
            status_code=200,
            content={
                "date": workout_date.isoformat(),
                "count": len(workouts),
                "workouts": workouts,
            },
        )

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch workouts: {str(exc)}",
        ) from exc


@app.get("/workouts/{date_str}", tags=["activities"])
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

        return JSONResponse(
            status_code=200,
            content={
                "date": workout_date.isoformat(),
                "count": len(workouts),
                "workouts": workouts,
            },
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch workouts for {date_str}: {str(exc)}",
        ) from exc


def _parse_bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


def _run_server(mode: str) -> None:
    if mode not in SERVER_MODES:
        supported_modes = ", ".join(sorted(SERVER_MODES))
        raise ValueError(
            f"Unsupported mode '{mode}'. Supported values: {supported_modes}"
        )

    defaults = SERVER_MODES[mode]

    host = os.getenv("API_HOST", defaults["host"])
    port = int(os.getenv("API_PORT", str(defaults["port"])))
    reload_enabled = _parse_bool_env("API_RELOAD", defaults["reload"])

    print(
        f"Starting My Garmin API in {mode} mode on http://{host}:{port}"
    )
    print(f"OpenAPI schema available at http://{host}:{port}/openapi.json")
    print(f"Interactive docs at http://{host}:{port}/docs")

    uvicorn.run(
        "my_garmin_api.api:app",
        host=host,
        port=port,
        reload=reload_enabled,
        reload_dirs=["my_garmin_api"] if reload_enabled else None,
    )


def main() -> None:
    """Run the FastAPI application with production defaults."""
    _run_server("production")


def main_dev() -> None:
    """Run the FastAPI application with development defaults and reload enabled."""
    _run_server("development")


if __name__ == "__main__":
    main()
