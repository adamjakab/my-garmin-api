"""Generic cache helpers for Garmin data aggregation."""

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any


DEFAULT_CACHE_FOLDER = "tmp"
DEFAULT_CACHE_EXPIRATION_SECONDS = 3600


def _get_cache_dir() -> Path:
    cache_dir = Path(os.getenv("GARMIN_CACHE_FOLDER", DEFAULT_CACHE_FOLDER)).expanduser()
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def _get_cache_expiration_seconds() -> int:
    return int(
        os.getenv(
            "GARMIN_CACHE_EXPIRATION_SECONDS",
            str(DEFAULT_CACHE_EXPIRATION_SECONDS),
        )
    )


def _build_cache_file_path(cache_key: str) -> Path:
    return _get_cache_dir() / f"{cache_key}.json"


def get_cache_key(*args: object) -> str:
    """Build a deterministic cache key from an arbitrary list of arguments."""
    raw_key = "cache-" + "-".join(str(arg) for arg in args)
    return hashlib.md5(raw_key.encode("utf-8")).hexdigest()


def load_cached_data(cache_key: str) -> Any | None:
    """Return cached data for the key, or None if unavailable or stale."""
    cache_file = _build_cache_file_path(cache_key)
    if not cache_file.exists():
        return None

    cache_age_seconds = time.time() - cache_file.stat().st_mtime
    if cache_age_seconds > _get_cache_expiration_seconds():
        cache_file.unlink(missing_ok=True)
        return None

    try:
        with cache_file.open("r", encoding="utf-8") as file_handle:
            return json.load(file_handle)
    except (OSError, json.JSONDecodeError):
        cache_file.unlink(missing_ok=True)
        return None


def save_cached_data(cache_key: str, data: Any) -> None:
    """Persist arbitrary JSON-serializable data into the configured cache."""
    cache_file = _build_cache_file_path(cache_key)
    with cache_file.open("w", encoding="utf-8") as file_handle:
        json.dump(data, file_handle, indent=2)