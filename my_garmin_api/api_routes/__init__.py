"""API route module discovery for the FastAPI application."""

from importlib import import_module
from pkgutil import iter_modules

from fastapi import APIRouter


def discover_routers() -> list[tuple[APIRouter, bool]]:
    """Return all routers with whether API-key auth should be enforced."""
    routers: list[tuple[APIRouter, bool]] = []

    for module_info in sorted(iter_modules(__path__), key=lambda item: item.name):
        if module_info.name.startswith("_"):
            continue

        module = import_module(f"{__name__}.{module_info.name}")
        router = getattr(module, "router", None)
        if isinstance(router, APIRouter):
            requires_api_key = bool(getattr(module, "REQUIRE_API_KEY", True))
            routers.append((router, requires_api_key))

    return routers
