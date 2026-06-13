---
description: Workspace instructions for the My Garmin API aggregation service
---

# My Garmin API — Workspace Instructions

This is a **Garmin Connect data enrichment service** that fetches comprehensive activity data and returns it as structured JSON through a RESTful API interface.

## OpenAPI Compatibility Guardrail

- For endpoints intended for ChatGPT Actions/tools via OpenAPI, do not use nullable date query parameters (for example `date | None`).
- Use required `date` query parameters and represent single-day lookups by setting `start_date` and `end_date` to the same date.

