"""Activity endpoint for the FastAPI application."""

from datetime import date
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

import my_garmin_api.garmin_fit as gfit


class ActivityTypeSchema(BaseModel):
    typeId: int = Field(
        title="Type ID",
        description="The numeric identifier for the activity type.",
    )
    typeKey: str = Field(
        title="Type Key",
        description="The string key identifying the activity type (e.g., 'running', 'cycling').",
    )


class ActivitySummarySchema(BaseModel):
    model_config = {
        "extra": "ignore", # allow|ignore|forbid
    }
    activityName: str = Field(
        title="Activity Name",
        description="The name of the activity as set by the user or device.",
    )
    startTimeLocal: str = Field(
        title="Start Time Local",
        description="The activity start time in the local timezone of the device, in ISO 8601 format.",
    )
    startTimeGMT: str = Field(
        title="Start Time GMT",
        description="The activity start time in GMT/UTC, in ISO 8601 format.",
    )
    activityType: ActivityTypeSchema
    distance: float = Field(
        title="Distance",
        description="Total distance of the activity in meters.",
    )
    duration: float = Field(
        title="Duration",
        description="Total duration of the activity in seconds.",
    )
    movingDuration: float = Field(
        title="Moving Duration",
        description="Duration the user was actively moving in seconds.",
    )
    elevationGain: float = Field(
        title="Elevation Gain",
        description="Total elevation gained during the activity in meters.",
    )
    elevationLoss: float = Field(
        title="Elevation Loss",
        description="Total elevation lost during the activity in meters.",
    )
    averageSpeed: float = Field(
        title="Average Speed",
        description="Average speed over the activity in meters per second.",
    )
    maxSpeed: float = Field(
        title="Max Speed",
        description="Maximum speed reached during the activity in meters per second.",
    )
    ownerDisplayName: str = Field(
        title="Owner Display Name",
        description="The Garmin display name of the activity owner.",
    )
    ownerFullName: str = Field(
        title="Owner Full Name",
        description="The full name of the activity owner.",
    )
    calories: float = Field(
        title="Calories",
        description="Estimated calories burned during the activity.",
    )
    bmrCalories: float = Field(
        title="BMR Calories",
        description="Estimated basal metabolic rate calories during the activity duration.",
    )
    averageHR: float = Field(
        title="Average Heart Rate",
        description="Average heart rate during the activity in beats per minute.",
    )
    maxHR: float = Field(
        title="Max Heart Rate",
        description="Maximum heart rate reached during the activity in beats per minute.",
    )
    averageRunningCadenceInStepsPerMinute: float = Field(
        title="Average Running Cadence",
        description="Average running cadence in steps per minute.",
    )
    maxRunningCadenceInStepsPerMinute: float = Field(
        title="Max Running Cadence",
        description="Maximum running cadence in steps per minute.",
    )
    steps: int = Field(
        title="Steps",
        description="Total number of steps recorded for the activity.",
    )
    sportTypeId: int = Field(
        title="Sport Type ID",
        description="Numeric identifier of the sport type reported by Garmin.",
    )
    avgPower: float = Field(
        title="Average Power",
        description="Average power output during the activity in watts.",
    )
    maxPower: float = Field(
        title="Max Power",
        description="Maximum power output during the activity in watts.",
    )
    aerobicTrainingEffect: float = Field(
        title="Aerobic Training Effect",
        description="Garmin aerobic training effect score for the activity.",
    )
    anaerobicTrainingEffect: float = Field(
        title="Anaerobic Training Effect",
        description="Garmin anaerobic training effect score for the activity.",
    )
    normPower: float = Field(
        title="Normalized Power",
        description="Normalized power estimate for the activity in watts.",
    )
    avgVerticalOscillation: float = Field(
        title="Average Vertical Oscillation",
        description="Average vertical oscillation during the activity in centimeters.",
    )
    avgGroundContactTime: float = Field(
        title="Average Ground Contact Time",
        description="Average ground contact time during the activity in milliseconds.",
    )
    avgStrideLength: float = Field(
        title="Average Stride Length",
        description="Average stride length during the activity in centimeters.",
    )
    vO2MaxValue: float = Field(
        title="VO2 Max Value",
        description="VO2 max estimate associated with the activity.",
    )
    avgVerticalRatio: float = Field(
        title="Average Vertical Ratio",
        description="Average vertical ratio during the activity.",
    )
    workoutId: int = Field(
        title="Workout ID",
        description="Identifier of the associated Garmin workout, if any.",
    )
    deviceId: int = Field(
        title="Device ID",
        description="Identifier of the Garmin device that recorded the activity.",
    )
    minTemperature: float = Field(
        title="Minimum Temperature",
        description="Minimum recorded temperature during the activity in Celsius.",
    )
    maxTemperature: float = Field(
        title="Maximum Temperature",
        description="Maximum recorded temperature during the activity in Celsius.",
    )
    minElevation: float = Field(
        title="Minimum Elevation",
        description="Minimum elevation recorded during the activity in meters.",
    )
    maxElevation: float = Field(
        title="Maximum Elevation",
        description="Maximum elevation recorded during the activity in meters.",
    )
    avgElevation: float = Field(
        title="Average Elevation",
        description="Average elevation during the activity in meters.",
    )
    maxDoubleCadence: float = Field(
        title="Max Double Cadence",
        description="Maximum double cadence value recorded during the activity.",
    )
    lapCount: int = Field(
        title="Lap Count",
        description="Number of laps recorded for the activity.",
    )
    locationName: str = Field(
        title="Location Name",
        description="Human-readable location associated with the activity.",
    )
    startLatitude: float = Field(
        title="Start Latitude",
        description="Latitude of the activity start point.",
    )
    startLongitude: float = Field(
        title="Start Longitude",
        description="Longitude of the activity start point.",
    )
    endLatitude: float = Field(
        title="End Latitude",
        description="Latitude of the activity end point.",
    )
    endLongitude: float = Field(
        title="End Longitude",
        description="Longitude of the activity end point.",
    )
    waterEstimated: float = Field(
        title="Water Estimated",
        description="Estimated water loss for the activity.",
    )
    trainingEffectLabel: str = Field(
        title="Training Effect Label",
        description="Garmin categorical label for training effect.",
    )
    activityTrainingLoad: float = Field(
        title="Activity Training Load",
        description="Training load score assigned to the activity.",
    )
    aerobicTrainingEffectMessage: str = Field(
        title="Aerobic Training Effect Message",
        description="Garmin message describing aerobic training effect.",
    )
    anaerobicTrainingEffectMessage: str = Field(
        title="Anaerobic Training Effect Message",
        description="Garmin message describing anaerobic training effect.",
    )
    moderateIntensityMinutes: int = Field(
        title="Moderate Intensity Minutes",
        description="Minutes spent in moderate intensity during the activity.",
    )
    vigorousIntensityMinutes: int = Field(
        title="Vigorous Intensity Minutes",
        description="Minutes spent in vigorous intensity during the activity.",
    )
    differenceBodyBattery: int = Field(
        title="Difference Body Battery",
        description="Net change in Body Battery during the activity.",
    )
    hrTimeInZone_1: float = Field(
        title="HR Time In Zone 1",
        description="Time spent in heart rate zone 1.",
    )
    hrTimeInZone_2: float = Field(
        title="HR Time In Zone 2",
        description="Time spent in heart rate zone 2.",
    )
    hrTimeInZone_3: float = Field(
        title="HR Time In Zone 3",
        description="Time spent in heart rate zone 3.",
    )
    hrTimeInZone_4: float = Field(
        title="HR Time In Zone 4",
        description="Time spent in heart rate zone 4.",
    )
    hrTimeInZone_5: float = Field(
        title="HR Time In Zone 5",
        description="Time spent in heart rate zone 5.",
    )
    powerTimeInZone_1: float = Field(
        title="Power Time In Zone 1",
        description="Time spent in power zone 1.",
    )
    powerTimeInZone_2: float = Field(
        title="Power Time In Zone 2",
        description="Time spent in power zone 2.",
    )
    powerTimeInZone_3: float = Field(
        title="Power Time In Zone 3",
        description="Time spent in power zone 3.",
    )
    powerTimeInZone_4: float = Field(
        title="Power Time In Zone 4",
        description="Time spent in power zone 4.",
    )
    powerTimeInZone_5: float = Field(
        title="Power Time In Zone 5",
        description="Time spent in power zone 5.",
    )
    endTimeGMT: str = Field(
        title="End Time GMT",
        description="Activity end timestamp in GMT/UTC, ISO 8601 format.",
    )
    activityUUID: str = Field(
        title="Activity UUID",
        description="Globally unique identifier of the activity.",
    )
    purposeful: bool = Field(
        title="Purposeful",
        description="Whether Garmin marks this activity as purposeful.",
    )
    pr: bool = Field(
        title="PR",
        description="Whether the activity includes a personal record.",
    )


class ActivitySchema(BaseModel):
    activity_id: int | None = None
    summary: ActivitySummarySchema
    errors: dict[str, str] | None = None


class ActivitiesResponseSchema(BaseModel):
    start_date: str = Field(
        title="Start Date",
        description="The start date of the requested range in YYYY-MM-DD format.",
    )
    end_date: str = Field(
        title="End Date",
        description="The end date of the requested range in YYYY-MM-DD format.",
    )
    count: int = Field(
        title="Count",
        description="The number of activities returned in the response for the selected date range.",
    )
    activities: list[ActivitySchema]


router = APIRouter(tags=["Activities"])


def _build_activity_response(
    start_date: date,
    end_date: date,
    activities: list[dict],
) -> ActivitiesResponseSchema:
    return ActivitiesResponseSchema(
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        count=len(activities),
        activities=[ActivitySchema.model_validate(a) for a in activities],
    )


@router.get(
    "/activities",
    summary="Fetch activities between two specific dates.",
    description="Fetch all activity data for a date range between the specified start and end dates. This endpoint can be used to fetch activities for a single date (start_date same as end_date) or to get activities between two specific dates.",
    operation_id="getActivitiesByDateRange",
    response_model=ActivitiesResponseSchema,
)
async def get_activities(
    start_date: date = Query(
        description="Start date in YYYY-MM-DD format. This is a required parameter.",
    ),
    end_date: date= Query(
        description="End date in YYYY-MM-DD format. This is a required parameter.",
    ),
) -> ActivitiesResponseSchema:
    """
    Fetch activities for an inclusive date range.

    **Parameters:**
    - `start_date`: Range start in YYYY-MM-DD format (required)
    - `end_date`: Range end in YYYY-MM-DD format (required)
    """
    if end_date < start_date:
        raise HTTPException(
            status_code=400,
            detail="end_date cannot be before start_date",
        )

    try:
        activities = gfit.get_activities_for_date_range(
            start_date=start_date,
            end_date=end_date,
        )
        return _build_activity_response(
            start_date,
            end_date,
            activities,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to fetch activities for "
                f"{start_date.isoformat()} to {end_date.isoformat()}: {str(exc)}"
            ),
        ) from exc
