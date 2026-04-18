"""Schema models for API routes."""

from my_garmin_api.api_routes.schemas.activities import (
    ActivitySchema,
    ActivitiesResponseSchema,
    ActivitySummarySchema,
    ActivityTypeSchema,
    AggregatedDetailsSchema,
    MetricStatSchema,
)

__all__ = [
    "ActivityTypeSchema",
    "ActivitySummarySchema",
    "MetricStatSchema",
    "AggregatedDetailsSchema",
    "ActivitySchema",
    "ActivitiesResponseSchema",
]
