"""Health endpoint for the FastAPI application.
DISABLED - This endpoint is currently disabled and will not be discovered.
"""

from pathlib import Path

from fastapi import APIRouter
import tomli

from my_garmin_api.api_routes.schemas.healthcheck import HealthResponseSchema


REQUIRE_API_KEY = False
router = APIRouter(tags=["Health"])
_PYPROJECT_PATH = Path(__file__).resolve().parents[2] / "pyproject.toml"


def _read_version_from_pyproject() -> str:
    """Return project version from pyproject.toml, or unknown if unavailable."""
    try:
        with _PYPROJECT_PATH.open("rb") as pyproject_file:
            pyproject = tomli.load(pyproject_file)
    except OSError:
        return "unknown"
    except tomli.TOMLDecodeError:
        return "unknown"

    project_section = pyproject.get("project")
    if isinstance(project_section, dict):
        version = project_section.get("version")
        if isinstance(version, str) and version.strip():
            return version.strip()

    return "unknown"


PROJECT_VERSION = _read_version_from_pyproject()


@router.get(
    "/",
    summary="Health check",
    description="Verify that the API service is running.",
    operation_id="getHealth",
    response_model=HealthResponseSchema,
)
async def get_health() -> HealthResponseSchema:
    """Return a simple health payload."""
    return HealthResponseSchema(
        status="ok",
        message="My Garmin API is running",
        version=PROJECT_VERSION,
    )
