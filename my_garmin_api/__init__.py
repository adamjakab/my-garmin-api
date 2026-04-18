"""My Garmin API package."""

from dotenv import load_dotenv

load_dotenv()

__all__ = ["api", "api_auth", "garmin_fit"]  # type: ignore
