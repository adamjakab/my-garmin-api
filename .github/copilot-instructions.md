---
description: Workspace instructions for the Garmin activity API aggregation service
---

# Garmin Activity API — Workspace Instructions

This is a **Garmin Connect data enrichment service** that fetches comprehensive activity data and returns it as structured JSON. It includes both CLI and RESTful API interfaces.

## Quick Links

- [Setup & Run Commands](../README.md#setup) — Poetry environment, .env configuration
- [Architecture & Data Flow](../README.md#run) — Activity fetching, enrichment pipeline, caching behavior
- [REST API Documentation](../README.md#rest-api-openapi--chatgpt) — OpenAPI schema, ChatGPT integration
- [Troubleshooting](../README.md#troubleshooting) — Rate limits, Cloudflare blocks, token persistence

## Project Structure

```
my_activity_api/
├── main.py                # CLI entry point: argument parsing, .env loading, main()
├── api.py                 # FastAPI REST server: OpenAPI schema, ChatGPT integration
├── garmin_fit.py         # Core logic: activity fetching, enrichment, caching (TTL=3600s)
├── __init__.py           # Package metadata
└── garminconnect/        # LOCAL FORK of python-garminconnect (PR #345)
    ├── client.py         # Garmin API client: 5-strategy authentication, token persistence
    ├── fit.py            # Binary FIT protocol encoder/decoder (workouts, activities)
    ├── workout.py        # Pydantic models: Workout, ExerciseSet, etc.
    └── exceptions.py     # Custom exception hierarchy
```

## Key Concepts

### Authentication & Token Reuse

The Garmin API endpoint enforces aggressive rate limiting (429). Token reuse is **essential**:

- `client.login()` uses a 5-strategy cascade (browser emulation → TLS impersonation via curl-cffi → fallback auth methods)
- Tokens persist to `~/.garminconnect` by default, or `GARMIN_TOKEN_STORE` env var
- **Always set `GARMIN_TOKEN_STORE`** in production to avoid re-authenticating every run
- MFA is handled via `prompt_mfa=lambda: input("MFA code: ")`

### Activity Enrichment Pattern

The `ACTIVITY_RESOURCE_FETCHERS` tuple in [garmin_fit.py](../my_activity_api/garmin_fit.py) defines 10+ resource types. Each activity is enriched with:

- `activity`: activity summary (HR, calories, distance)
- `details`: full activity chart, splits, lap data
- `splits`, `typed_splits`, `split_summaries`: workout segmentation
- `weather`: conditions at activity time/location
- `hr_time_in_zones`, `power_time_in_zones`: zone distributions
- `exercise_sets`, `gear`: exercise details, equipment used

**Error Resilience:** The `_safe_fetch_activity_resource()` wrapper catches per-resource errors. If one endpoint fails, the activity is returned with an `errors` dict instead of failing the entire request. This is intentional.

### Caching

- **Location:** `tmp/workouts_YYYY-MM-DD.json` (or custom `--tmp-dir`)
- **TTL:** 1 hour (hardcoded in `get_workouts_for_date()`)
- **Behavior:** Successive requests for the same date return cached data; if >1 hour old, cache is deleted and fresh data is fetched
- **Manual clear:** `rm tmp/workouts_*.json` to force refresh (cache files expire naturally)

## Development Conventions

### Code Style

- **Python 3.10+** strict (`requires-python = ">=3.10,<4.0"`)
- **Type hints** enforced (uses `|` operator, not `Union`)
- **Docstrings** on public functions and modules
- **Pylint**: configured in `pyproject.toml`, excludes `garminconnect/` (external code)
- **VS Code**: `.vscode/settings.json` excludes `garminconnect/` from strict Python analysis

### Exception Handling

Use custom exceptions from `garminconnect.exceptions`:

- `GarminConnectConnectionError` — Network/communication failures
- `GarminConnectTooManyRequestsError` — 429 rate limit (wait before retry, reuse tokens)
- `GarminConnectAuthenticationError` — Invalid credentials or auth failures
- `GarminConnectInvalidFileFormatError` — Malformed FIT protocol data

### Configuration

All configuration comes from `.env` (auto-loaded in `main.py` via `python-dotenv`):

- **GARMIN_EMAIL** (required): Garmin Connect account email
- **GARMIN_PASSWORD** (required): Garmin Connect password
- **GARMIN_TOKEN_STORE** (optional, recommended): Path to token storage (e.g., `~/.garminconnect`)
- **API_HOST** (optional): API server host (default: `127.0.0.1`)
- **API_PORT** (optional): API server port (default: `8000`)
- **API_RELOAD** (optional): Enable auto-reload on code changes (default: `false`)

When adding or removing environment variables, **update the README**.

## Testing & Linting

- **No test suite** exists (zero test infrastructure)
- **Linting:** Run `pylint my_activity_api/` (excludes `garminconnect/` per config)
- **Type checking:** VS Code Pylance with strict mode; `garminconnect/` marked as external

## Common Pitfalls

| Issue | Cause | Solution |
|-------|-------|----------|
| **429 Rate Limit** | Garmin throttles auth endpoints | Set `GARMIN_TOKEN_STORE` to reuse tokens; don't immediately retry auth |
| **Cloudflare Blocks Login** | Plain requests detected as bots | Requires `curl-cffi` (in dependencies); must be installed |
| **"Wrong Credentials" Error** | Invalid email/password or MFA prompt missed | Verify `.env` values; watch for MFA prompt in terminal when first authenticating |
| **First Login Hangs** | Previous session still active or rate limit not cleared | Wait ~5min before retrying; check if another instance is running |
| **Cache Not Expiring** | Check file mtime, not modification time | TTL is 1 hour from cache creation; `rm tmp/workouts_*.json` to force refresh |
| **Missing Data in Output** | Some activities lack certain resources (e.g., no weather, no gear) | Check `errors` dict in output; handled gracefully; activity still returned |
| **Garminconnect Import Fails** | Using pip-installed `garminconnect` instead of local fork | Ensure Poetry is using `.venv`; this project uses local PR #345 fork, not PyPI package |

## When Modifying Code

### Adding Dependencies

1. Edit `pyproject.toml`
2. Run `poetry lock`
3. Run `poetry install` to activate in `.venv`
4. Test: `poetry run app --test-auth` or `poetry run app --date <date>`

### Modifying `garminconnect/`

⚠️ **This is a local fork of PR #345.** It's not the standard PyPI package. The PR contains critical fixes not yet in the main branch. When making changes:

- Document the reason (why we can't use upstream)
- Keep changes minimal; consider contributing them back to the official repo
- Don't modify `garminconnect/` without understanding the specific PR it's based on

### Adding New Enrichment Resources

1. Create a lambda in `ACTIVITY_RESOURCE_FETCHERS` (in [garmin_fit.py](../my_activity_api/garmin_fit.py))
2. Use the `_safe_fetch_activity_resource()` wrapper (resilience to per-resource errors)
3. Update this instructions file with the new resource in the "Activity Enrichment" section
4. Update the README if it describes the output schema

### Adding CLI Arguments

1. Edit `main.py`: add argument to `argparse` in `_create_parser()`
2. Pass argument to `get_workouts_for_date()` if it affects behavior
3. Document the argument in README

### Adding REST API Endpoints

1. Edit `api.py`: add route function with `@app.get()` or `@app.post()` decorator
2. Use FastAPI parameter annotations (`Query`, `Path`, etc.) for automatic OpenAPI schema generation
3. Include comprehensive docstring with parameter descriptions (auto-included in schema)
4. Return proper HTTP status codes and error handling (`HTTPException` for 4xx/5xx)
5. Update README.md "REST API" section with endpoint documentation and examples
6. Test with interactive docs: `http://localhost:8000/docs` while API is running
7. Verify updated OpenAPI schema: `http://localhost:8000/openapi.json`

### Extending the Caching System

1. Cache file location is in `get_workouts_for_date()` — modify with caution
2. TTL is hardcoded to 3600 seconds; mark as TODO if making configurable
3. Update `.github/copilot-instructions.md` Caching section if behavior changes
4. Test cache expiry: `rm tmp/workouts_*.json && poetry run app --date 2026-04-01` (twice to verify cache reuse)

## File Modification Guidelines

When editing files, maintain consistency with existing patterns:

- **main.py**: Keep CLI logic in `_parse_date()`, `_create_parser()`, and `main()`; delegate business logic to `garmin_fit.py`
- **api.py**: Use FastAPI decorators and parameter annotations for route definition; add comprehensive docstrings for OpenAPI schema generation; reuse `get_workouts_for_date()` from `garmin_fit.py`
- **garmin_fit.py**: Use the lambda + `_safe_fetch_activity_resource()` pattern for new resource fetchers; add docstrings for new functions
- **garminconnect/**: Minimal changes; document why local fork is necessary if modifying
- **README.md**: Link to specific line ranges; keep setup/run/troubleshooting sections synchronized with code behavior

---

**Last Updated:** April 2026 | **Python:** 3.10+ | **Package Manager:** Poetry 2.x | **API Framework:** FastAPI 0.100+
