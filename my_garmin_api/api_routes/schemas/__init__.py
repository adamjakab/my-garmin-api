"""Schema models for API routes."""

from my_garmin_api.api_routes.schemas.activities import ActivitiesResponseSchema
from my_garmin_api.api_routes.schemas.activity import ActivitySchema
from my_garmin_api.api_routes.schemas.activity_details import (
    AggregatedDetailsSchema,
    MetricStatSchema,
    MetricsSchema,
)
from my_garmin_api.api_routes.schemas.activity_splits import (
    ActivitySplitsSchema,
    LapSchema,
    SplitEventSchema,
    SplitSectionTypeSchema,
)
from my_garmin_api.api_routes.schemas.activity_summary import (
    ActivitySummarySchema,
    ActivityTypeSchema,
)

__all__ = [
    "ActivityTypeSchema",
    "ActivitySummarySchema",
    "MetricStatSchema",
    "MetricsSchema",
    "AggregatedDetailsSchema",
    "SplitSectionTypeSchema",
    "SplitEventSchema",
    "LapSchema",
    "ActivitySplitsSchema",
    "ActivitySchema",
    "ActivitiesResponseSchema",
]
