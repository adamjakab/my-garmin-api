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
from my_garmin_api.api_routes.schemas.activity_gear import ActivityGearSchema
from my_garmin_api.api_routes.schemas.healthcheck import HealthResponseSchema
from my_garmin_api.api_routes.schemas.hrv import HrvEntrySchema, HrvResponseSchema
from my_garmin_api.api_routes.schemas.rhr import RhrEntrySchema, RhrResponseSchema
from my_garmin_api.api_routes.schemas.weight import WeightEntrySchema, WeightResponseSchema
from my_garmin_api.api_routes.schemas.activity_hr_time_in_zones import (
    HrTimeInZoneSchema,
)
from my_garmin_api.api_routes.schemas.activity_power_time_in_zones import (
    PowerTimeInZoneSchema,
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
from my_garmin_api.api_routes.schemas.activity_weather import (
    ActivityWeatherSchema,
    WeatherStationSchema,
    WeatherTypeSchema,
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
    "PowerTimeInZoneSchema",
    "ActivityWeatherSchema",
    "WeatherStationSchema",
    "WeatherTypeSchema",
    "ActivityGearSchema",
    "HealthResponseSchema",
    "HrvEntrySchema",
    "HrvResponseSchema",
    "RhrEntrySchema",
    "RhrResponseSchema",
    "WeightEntrySchema",
    "WeightResponseSchema",
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
