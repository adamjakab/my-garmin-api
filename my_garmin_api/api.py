"""FastAPI application for exposing Garmin workout data via HTTP API with OpenAPI schema."""

import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import uvicorn

from my_garmin_api.api_auth import (
    API_KEY_HEADER_NAME,
    require_api_key,
    validate_api_key,
)
from my_garmin_api.api_routes import discover_routers

load_dotenv()

app = FastAPI(
    title="My Garmin API",
    description="REST API for fetching and caching Garmin Connect workout data. "
    "Use the [/openapi.json](./openapi.json) endpoint to retrieve the OpenAPI 3.0 schema for ChatGPT GPT integration.",
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

AUTH_EXEMPT_PATHS = {"/docs", "/openapi.json"}

for router in discover_routers():
    app.include_router(router, dependencies=[Depends(require_api_key)])


@app.middleware("http")
async def enforce_api_key(request: Request, call_next):
    """Require the configured API key for every incoming request."""
    if request.url.path in AUTH_EXEMPT_PATHS:
        return await call_next(request)

    try:
        validate_api_key(request.headers.get(API_KEY_HEADER_NAME))
    except HTTPException as exc:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    return await call_next(request)


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

    print(f"Starting My Garmin API in {mode} mode on http://{host}:{port}")
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
