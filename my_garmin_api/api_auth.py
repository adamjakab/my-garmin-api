"""API authentication helpers."""

import os
import secrets

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader


API_KEY_HEADER_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_HEADER_NAME, auto_error=False)


def _get_expected_api_key() -> str:
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise RuntimeError("API_KEY must be configured in the environment.")

    return api_key


def validate_api_key(provided_api_key: str | None) -> None:
    """Raise an HTTP error if the provided API key is missing or invalid."""
    expected_api_key = _get_expected_api_key()
    if provided_api_key and secrets.compare_digest(provided_api_key, expected_api_key):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API key.",
    )


async def require_api_key(
    provided_api_key: str | None = Security(api_key_header),
) -> str:
    """Validate the API key provided in the request headers."""
    validate_api_key(provided_api_key)
    return provided_api_key or ""