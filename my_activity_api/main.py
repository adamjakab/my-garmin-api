from argparse import ArgumentParser
from datetime import date
import json
from dotenv import load_dotenv
import my_activity_api.garmin_fit as gfit

load_dotenv()

def _parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("Date must use YYYY-MM-DD format") from exc


def main() -> None:
    parser = ArgumentParser(description="Fetch Garmin workout data for a date")
    parser.add_argument(
        "--date",
        dest="workout_date",
        type=_parse_date,
        default=date.today(),
        help="Workout date in YYYY-MM-DD format. If omitted, uses today.",
    )
    parser.add_argument(
        "--tmp-dir",
        default="tmp",
        help="Output directory for FIT files (default: tmp)",
    )
    parser.add_argument(
        "--test-auth",
        action="store_true",
        help="Test Garmin authentication only (no download)",
    )
    args = parser.parse_args()

    res = gfit.test()
    if not res:
        raise SystemExit("Garmin authentication failed. Check credentials and try again.")
    
    activity_data = gfit.get_workouts_for_date(args.workout_date)
    print(json.dumps(activity_data, indent=2))
    
    # try:
        
    # except (RuntimeError, ValueError) as exc:
    #     raise SystemExit(f"Error: {exc}") from exc

    # print("Done!")


if __name__ == "__main__":
    main()
