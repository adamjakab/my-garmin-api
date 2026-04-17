"""Health endpoints for the FastAPI application."""

from fastapi import APIRouter


router = APIRouter(tags=["health"])


@router.get("/")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "message": "My Garmin API is running."}
