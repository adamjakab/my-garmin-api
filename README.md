# My Garmin API (`my-garmin-api`)

Python project to make your Garmin data accessible through the API you were never given.

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

Cache behavior:

- Results are cached in `tmp/workouts_YYYY-MM-DD.json` (or the directory passed to `--tmp-dir`).
- Successive requests for the same date use the cached file.
- If the cache file is older than 1 hour, it is deleted and fresh data is fetched from Garmin Connect.

The output is a JSON array. Each item represents one workout found for that date and includes:

- `summary`: the activity returned by Garmin's activity search endpoint for that date
- `activity`: the per-activity summary endpoint payload
- `details`: chart and lap/detail payload
- `splits`, `typed_splits`, `split_summaries`
- `weather`, `hr_time_in_zones`, `power_time_in_zones`
- `exercise_sets`, `gear`
- `errors`: optional per-resource errors when Garmin exposes the activity but one enrichment endpoint fails

For Python usage, call `get_workouts_for_date(...)` from [my_garmin_api/garmin_fit.py](my_garmin_api/garmin_fit.py).

## REST API (OpenAPI / ChatGPT)

The project includes a FastAPI-based REST API that exposes cached workouts via HTTP. This is ideal for integrating with ChatGPT GPTs or other services requiring OpenAPI 3.0 schema.

### Start the API Server

```bash
source .venv/bin/activate
poetry run api
```

By default, the API runs on `http://127.0.0.1:8000`.

### API Configuration

Set these optional environment variables in `.env`:

- **API_HOST**: Server host (default: `127.0.0.1`)
- **API_PORT**: Server port (default: `8000`)
- **API_RELOAD**: Auto-reload on code changes (default: `false`)

Example:

```dotenv
API_HOST=0.0.0.0
API_PORT=5000
API_RELOAD=true
```

### Endpoints

#### GET / (Health Check)

```bash
curl http://localhost:8000/
```

Response:

```json
{
 "status": "ok",
 "message": "My Garmin API is running"
}
```

#### GET /workouts (Query Parameter)

Fetch workouts for a specific date using query parameter.

```bash
# Today's workouts
curl http://localhost:8000/workouts

# Specific date
curl "http://localhost:8000/workouts?date=2026-04-09"

# With custom cache TTL (seconds)
curl "http://localhost:8000/workouts?date=2026-04-09&cache_ttl_seconds=7200"
```

Response:

```json
{
 "date": "2026-04-09",
 "count": 2,
 "workouts": [
  {
   "activity_id": 12345,
   "summary": { ... },
   "activity": { ... },
   "details": { ... },
   "splits": [ ... ],
   "weather": { ... },
   "hr_time_in_zones": { ... },
   "power_time_in_zones": { ... },
   "exercise_sets": [ ... ],
   "gear": [ ... ],
   "errors": {}
  }
 ]
}
```

#### GET /workouts/{date} (Path Parameter)

Alternative endpoint using path parameter instead of query string.

```bash
curl http://localhost:8000/workouts/2026-04-09
```

### OpenAPI Schema (ChatGPT Integration)

The OpenAPI 3.0 schema is automatically generated and available at:

```txt
http://localhost:8000/openapi.json
```

**To use with ChatGPT GPTs:**

1. Start the API server: `poetry run api`
2. Expose the API (e.g., via ngrok, tunnel, or cloud deployment): `ngrok http 8000`
3. In ChatGPT GPT settings, add schema URL: `https://<your-domain>/openapi.json`
4. Test in ChatGPT by asking it to fetch workouts for a specific date

**Example Schema URL Formats:**

- Local testing: `http://localhost:8000/openapi.json`
- ngrok tunnel: `https://abc123.ngrok.io/openapi.json`
- Cloud deployment (AWS, GCP, etc.): `https://api.example.com/openapi.json`

### Interactive Documentation

While developing, access the interactive API docs:

```txt
http://localhost:8000/docs         # Swagger UI
http://localhost:8000/redoc        # ReDoc
```

### Response Schema

Each workout in the `workouts` array includes:

- **activity_id**: Garmin activity ID
- **summary**: Activity metadata (time, distance, calories, HR)
- **activity**: Per-activity summary endpoint
- **details**: Full activity chart, splits, lap data
- **splits**, **typed_splits**, **split_summaries**: Workout segmentation
- **weather**: Conditions at activity time/location
- **hr_time_in_zones**: Heart rate zone time distribution
- **power_time_in_zones**: Power zone time distribution (if available)
- **exercise_sets**: Exercise details (if strength training)
- **gear**: Equipment used
- **errors**: Dict of per-resource errors (if any endpoint fails during enrichment)

### Caching

The API reuses the same caching mechanism as the CLI:

- Results are cached in `tmp/workouts_YYYY-MM-DD.json`
- Default TTL: 1 hour (3600 seconds)
- Override via `?cache_ttl_seconds=` query parameter
- Manual clear: `rm tmp/workouts_*.json` to force refresh on next request

## Notes

- Project-local Poetry config is in `poetry.toml` with `virtualenvs.create = true` and `virtualenvs.in-project = true`.
- Poetry creates and manages the environment in `.venv`.

## Troubleshooting

- If Garmin returns 429 or Cloudflare blocks login, stop retries and wait before trying again.
- Set `GARMIN_TOKEN_STORE` (for example `~/.garminconnect`) so tokens can be reused instead of re-authenticating every run.
- First successful login may require waiting until the rate limit clears.
