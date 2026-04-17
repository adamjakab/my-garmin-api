# My Garmin API (`my-garmin-api`)

> **Warning**
> This project is not production ready yet!

Python project to make your Garmin data accessible through a FastAPI service.

## Requirements

- Python 3.10+
- Poetry 2.x
- Garmin Connect account credentials

## Environment Variables

- GARMIN_EMAIL: Garmin Connect email
- GARMIN_PASSWORD: Garmin Connect password
- GARMIN_TOKEN_STORE (optional): token storage directory/file path passed to `client.login(...)`
- API_KEY: shared secret required in the `X-API-Key` request header

Create a local `.env` file in the project root:

```dotenv
GARMIN_EMAIL=your@email.com
GARMIN_PASSWORD=your-password
# Optional:
# GARMIN_TOKEN_STORE=~/.garminconnect
API_KEY=replace-with-a-strong-random-value
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

Start the API server:

```bash
source .venv/bin/activate
poetry run api
```

Fetch all activities for today as JSON:

```bash
curl http://localhost:8000/activities
```

Fetch activities for a specific day as JSON:

```bash
curl "http://localhost:8000/activities?start_date=2026-04-01"
```

Fetch activities for a date range as JSON:

```bash
curl "http://localhost:8000/activities?start_date=2026-04-01&end_date=2026-04-03"
```

Cache behavior:

- Results are cached in date-range JSON files under the folder configured by `GARMIN_CACHE_FOLDER`.
- Successive API requests for the same date use the cached file.
- If the cache file is older than `GARMIN_CACHE_EXPIRATION_SECONDS`, it is deleted and fresh data is fetched from Garmin Connect.

The API returns a JSON object with `start_date`, `end_date`, `count`, and `activities`. Each activity includes:

- `summary`: the activity returned by Garmin's activity search endpoint for that date
- `activity`: the per-activity summary endpoint payload
- `details`: chart and lap/detail payload
- `splits`, `typed_splits`, `split_summaries`
- `weather`, `hr_time_in_zones`, `power_time_in_zones`
- `exercise_sets`, `gear`
- `errors`: optional per-resource errors when Garmin exposes the activity but one enrichment endpoint fails

For Python usage, call `get_activities_for_date_range(start_date, end_date)` from [my_garmin_api/garmin_fit.py](my_garmin_api/garmin_fit.py).

## REST API (OpenAPI / ChatGPT)

The project exposes cached activities through FastAPI. This is the supported interface for local use, integrations, and OpenAPI-based tooling.

All API endpoints require the `X-API-Key` header to match the configured `API_KEY` value.

The documentation routes `/docs` and `/openapi.json` are exempt so you can browse the schema without the header. The actual API endpoints still require `X-API-Key`.

### Start the API Server

```bash
source .venv/bin/activate
poetry run api-dev
```

Use one of these commands depending on the mode you want:

```bash
poetry run api-dev   # development, auto-reload enabled
poetry run api       # production defaults, no reload
```

By default, development runs on `http://127.0.0.1:8000` and production runs on `http://0.0.0.0:8000`.

### API Configuration

Set these optional environment variables in `.env`:

- **API_HOST**: Server host (default: `127.0.0.1`)
- **API_PORT**: Server port (default: `8000`)
- **API_RELOAD**: Override auto-reload behavior for the selected mode

Example:

```dotenv
API_HOST=127.0.0.1
API_PORT=5000
API_RELOAD=true
```

Recommended workflow:

- Development: run `poetry run api-dev` and let Uvicorn reload whenever files under `my_garmin_api/` change.
- Production: run `poetry run api`.

### Endpoints

#### GET / (Health Check)

```bash
curl http://localhost:8000/

# With API key
curl -H "X-API-Key: <your-api-key>" http://localhost:8000/
```

Response:

```json
{
 "status": "ok",
 "message": "My Garmin API is running"
}
```

#### GET /activities

Fetch activities for a single day or inclusive date range using query parameters.

```bash
# Today's activities
curl -H "X-API-Key: <your-api-key>" http://localhost:8000/activities

# Specific day
curl -H "X-API-Key: <your-api-key>" "http://localhost:8000/activities?start_date=2026-04-09"

# Date range
curl -H "X-API-Key: <your-api-key>" "http://localhost:8000/activities?start_date=2026-04-09&end_date=2026-04-11"
```

Response:

```json
{
 "start_date": "2026-04-09",
 "end_date": "2026-04-11",
 "count": 2,
 "activities": [
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

### OpenAPI Schema (ChatGPT Integration)

The OpenAPI 3.0 schema is automatically generated and available at:

```txt
http://localhost:8000/openapi.json
```

**To use with ChatGPT GPTs:**

1. Start the API server: `poetry run api`
2. Expose the API (e.g., via ngrok, tunnel, or cloud deployment): `ngrok http 8000`
3. In ChatGPT GPT settings, add schema URL: `https://<your-domain>/openapi.json`
4. Test in ChatGPT by asking it to fetch activities for a specific date

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

Each activity in the `activities` array includes:

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

The API uses date-based JSON cache files:

- Results are cached in the folder configured by `GARMIN_CACHE_FOLDER`
- Default TTL comes from `GARMIN_CACHE_EXPIRATION_SECONDS` (3600 seconds if unset)
- Manual clear: remove the JSON files from your configured cache folder to force refresh on next request

## Notes

- Project-local Poetry config is in `poetry.toml` with `virtualenvs.create = true` and `virtualenvs.in-project = true`.
- Poetry creates and manages the environment in `.venv`.

## Troubleshooting

- If Garmin returns 429 or Cloudflare blocks login, stop retries and wait before trying again.
- Set `GARMIN_TOKEN_STORE` (for example `~/.garminconnect`) so tokens can be reused instead of re-authenticating every run.
- First successful login may require waiting until the rate limit clears.
