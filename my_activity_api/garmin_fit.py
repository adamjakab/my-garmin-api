"""GArmin FIT file handling."""

import os
from datetime import date
from pathlib import Path
import sys


from .garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)


def do_it(workout_date: date | None = None, tmp_dir: str = "tmp"):
    """Basic usage example."""
    _ = tmp_dir

    api = init_api()
    if not api:
        return

    if not workout_date:
        workout_date = date.today()

    full_name = api.get_full_name() or ""
    first_name = full_name.split()[0] if full_name.strip() else "Unknown User"
    print(f"Welcome to Garmin. You are: {first_name}.")
    
    hr = api.get_heart_rates(workout_date.isoformat())
    if hr:
        print(f"Resting HR  : {hr.get('restingHeartRate', 'n/a')} bpm")
    
    # data = api.get_activities(0, 1)
    # print (f"Garmin data: {data}")

def init_api() -> Garmin | None:
    """Initialise Garmin API, restoring saved tokens or logging in fresh."""

    tokenstore = os.getenv("GARMIN_TOKEN_STORE") or "~/.garminconnect"
    tokenstore_path = str(Path(tokenstore).expanduser())

    # Try to restore saved tokens
    try:
        garmin = Garmin()
        garmin.login(tokenstore_path)
        print("Authenticated using saved tokens.")
        return garmin

    except GarminConnectTooManyRequestsError as err:
        print(f"Rate limit: {err}")
        sys.exit(1)

    except (GarminConnectAuthenticationError, GarminConnectConnectionError):
        print("No valid tokens found. Proceeding to login...")

    # Fresh credential login with MFA support
    while True:
        try:
            email = os.getenv("GARMIN_EMAIL")
            password = os.getenv("GARMIN_PASSWORD")

            if not email or not password:
                raise RuntimeError(
                    "GARMIN_EMAIL and GARMIN_PASSWORD must be set in the environment or .env file."
                )

            garmin = Garmin(
                email=email,
                password=password,
                prompt_mfa=lambda: input("MFA code: ").strip(),
            )
            garmin.login(tokenstore_path)
            print(f"Login successful. Tokens saved to: {tokenstore_path}")
            return garmin

        except GarminConnectTooManyRequestsError as err:
            print(f"Rate limit: {err}")
            sys.exit(1)

        except GarminConnectAuthenticationError:
            print("Wrong credentials.")
            return None

        except GarminConnectConnectionError as err:
            print(f"Connection error: {err}")
            return None

        except KeyboardInterrupt:
            return None
