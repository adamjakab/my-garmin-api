"""API route module discovery for the FastAPI application."""

from importlib import import_module
from pkgutil import iter_modules

from fastapi import APIRouter


def discover_routers() -> list[APIRouter]:
    """Return all APIRouter instances exposed as `router` in this package."""
    routers: list[APIRouter] = []

    for module_info in sorted(iter_modules(__path__), key=lambda item: item.name):
        if module_info.name.startswith("_"):
            continue

        module = import_module(f"{__name__}.{module_info.name}")
        router = getattr(module, "router", None)
        if isinstance(router, APIRouter):
            routers.append(router)

    return routers