"""Schema models for API routes."""

from my_garmin_api.api_routes.schemas.activities import ActivitiesResponseSchema
from my_garmin_api.api_routes.schemas.activity import ActivitySchema
from my_garmin_api.api_routes.schemas.activity_details import (
    AggregatedDetailsSchema,
    MetricStatSchema,
    MetricsSchema,
)
from my_garmin_api.api_routes.schemas.activity_exercise_sets import (
    ActivityExerciseSetsSchema,
    ExerciseSetEntrySchema,
    ExerciseSetExerciseSchema,
)
from my_garmin_api.api_routes.schemas.activity_hr_time_in_zones import (
    HrTimeInZoneSchema,
)
from my_garmin_api.api_routes.schemas.activity_splits import (
    ActivitySplitsSchema,
    LapSchema,
    SplitEventSchema,
    SplitSectionTypeSchema,
)
from my_garmin_api.api_routes.schemas.activity_split_summaries import (
    ActivitySplitSummariesSchema,
    SplitSummarySchema,
)
from my_garmin_api.api_routes.schemas.activity_summary import (
    ActivitySummarySchema,
    ActivityTypeSchema,
)
from my_garmin_api.api_routes.schemas.activity_typed_splits import (
    ActivityTypedSplitsSchema,
    ActivityUuidSchema,
    TypedSplitSchema,
)

__all__ = [
    "ActivityTypeSchema",
    "ActivitySummarySchema",
    "MetricStatSchema",
    "MetricsSchema",
    "AggregatedDetailsSchema",
    "ExerciseSetExerciseSchema",
    "ExerciseSetEntrySchema",
    "ActivityExerciseSetsSchema",
    "HrTimeInZoneSchema",
    "SplitSectionTypeSchema",
    "SplitEventSchema",
    "LapSchema",
    "ActivitySplitsSchema",
    "SplitSummarySchema",
    "ActivitySplitSummariesSchema",
    "ActivityUuidSchema",
    "TypedSplitSchema",
    "ActivityTypedSplitsSchema",
    "ActivitySchema",
    "ActivitiesResponseSchema",
]
