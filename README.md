# my-activity-api

Poetry-based Python project using a local virtual environment in `.venv`.

## Requirements

- Python 3.10+
- Poetry 2.x
- Garmin Connect account credentials

## Environment Variables

- GARMIN_EMAIL: Garmin Connect email
- GARMIN_PASSWORD: Garmin Connect password
- GARMIN_TOKEN_STORE (optional): token storage directory/file path passed to `client.login(...)`

Create a local `.env` file in the project root:

```dotenv
GARMIN_EMAIL=your@email.com
GARMIN_PASSWORD=your-password
# Optional:
# GARMIN_TOKEN_STORE=~/.garminconnect
```

The app loads `.env` automatically at runtime via `python-dotenv`.

## Setup

1. Create local env:

```bash
poetry install
```

1. Activate env:

```bash
source .venv/bin/activate
```

1. (Optional) Verify Poetry environment path:

```bash
poetry env info
```

## Run

```bash
source .venv/bin/activate
poetry run app
```

Fetch all workouts for today as JSON:

```bash
poetry run app
```

Fetch all workouts for a specific date as JSON:

```bash
poetry run app --date 2026-04-01
```

The output is a JSON array. Each item represents one workout found for that date and includes:

- `summary`: the activity returned by Garmin's activity search endpoint for that date
- `activity`: the per-activity summary endpoint payload
- `details`: chart and lap/detail payload
- `splits`, `typed_splits`, `split_summaries`
- `weather`, `hr_time_in_zones`, `power_time_in_zones`
- `exercise_sets`, `gear`
- `errors`: optional per-resource errors when Garmin exposes the activity but one enrichment endpoint fails

For Python usage, call `get_workouts_for_date(...)` from [my_activity_api/garmin_fit.py](/home/jackisback/WslCode/garmin/my-activity-api/my_activity_api/garmin_fit.py).

## Notes

- Project-local Poetry config is in `poetry.toml` with `virtualenvs.create = true` and `virtualenvs.in-project = true`.
- Poetry creates and manages the environment in `.venv`.

## Troubleshooting

- If Garmin returns 429 or Cloudflare blocks login, stop retries and wait before trying again.
- Set `GARMIN_TOKEN_STORE` (for example `~/.garminconnect`) so tokens can be reused instead of re-authenticating every run.
- First successful login may require waiting until the rate limit clears.
