from typing import Any, Optional

from pydantic import BaseModel, Field


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
        "extra": "ignore",  # allow|ignore|forbid
    }

    activityName: Optional[str] = Field(
        default=None,
        title="Activity Name",
        description="The name of the activity as set by the user or device.",
    )

    startTimeLocal: Optional[str] = Field(
        default=None,
        title="Start Time Local",
        description="The activity start time in the local timezone of the device, in ISO 8601 format.",
    )

    startTimeGMT: Optional[str] = Field(
        default=None,
        title="Start Time GMT",
        description="The activity start time in GMT/UTC, in ISO 8601 format.",
    )

    endTimeGMT: Optional[str] = Field(
        default=None,
        title="End Time GMT",
        description="Activity end timestamp in GMT/UTC, ISO 8601 format.",
    )

    distance: Optional[float] = Field(
        default=None,
        title="Distance",
        description="Total distance of the activity in meters.",
    )

    duration: Optional[float] = Field(
        default=None,
        title="Duration",
        description="Total duration of the activity in seconds.",
    )

    movingDuration: Optional[float] = Field(
        default=None,
        title="Moving Duration",
        description="Duration the user was actively moving in seconds.",
    )

    elevationGain: Optional[float] = Field(
        default=None,
        title="Elevation Gain",
        description="Total elevation gained during the activity in meters.",
    )

    elevationLoss: Optional[float] = Field(
        default=None,
        title="Elevation Loss",
        description="Total elevation lost during the activity in meters.",
    )

    averageSpeed: Optional[float] = Field(
        default=None,
        title="Average Speed",
        description="Average speed over the activity in meters per second.",
    )

    maxSpeed: Optional[float] = Field(
        default=None,
        title="Max Speed",
        description="Maximum speed reached during the activity in meters per second.",
    )

    ownerDisplayName: Optional[str] = Field(
        default=None,
        title="Owner Display Name",
        description="The Garmin display name of the activity owner.",
    )

    ownerFullName: Optional[str] = Field(
        default=None,
        title="Owner Full Name",
        description="The full name of the activity owner.",
    )

    calories: Optional[float] = Field(
        default=None,
        title="Calories",
        description="Estimated calories burned during the activity.",
    )

    bmrCalories: Optional[float] = Field(
        default=None,
        title="BMR Calories",
        description="Estimated basal metabolic rate calories during the activity duration.",
    )

    averageHR: Optional[float] = Field(
        default=None,
        title="Average Heart Rate",
        description="Average heart rate during the activity in beats per minute.",
    )

    maxHR: Optional[float] = Field(
        default=None,
        title="Max Heart Rate",
        description="Maximum heart rate reached during the activity in beats per minute.",
    )

    averageRunningCadenceInStepsPerMinute: Optional[float] = Field(
        default=None,
        title="Average Running Cadence",
        description="Average running cadence in steps per minute.",
    )

    maxRunningCadenceInStepsPerMinute: Optional[float] = Field(
        default=None,
        title="Max Running Cadence",
        description="Maximum running cadence in steps per minute.",
    )

    steps: Optional[int] = Field(
        default=None,
        title="Steps",
        description="Total number of steps recorded for the activity.",
    )

    sportTypeId: Optional[int] = Field(
        default=None,
        title="Sport Type ID",
        description="Numeric identifier of the sport type reported by Garmin.",
    )

    avgPower: Optional[float] = Field(
        default=None,
        title="Average Power",
        description="Average power output during the activity in watts.",
    )

    maxPower: Optional[float] = Field(
        default=None,
        title="Max Power",
        description="Maximum power output during the activity in watts.",
    )

    aerobicTrainingEffect: Optional[float] = Field(
        default=None,
        title="Aerobic Training Effect",
        description="Garmin aerobic training effect score for the activity.",
    )

    anaerobicTrainingEffect: Optional[float] = Field(
        default=None,
        title="Anaerobic Training Effect",
        description="Garmin anaerobic training effect score for the activity.",
    )

    normPower: Optional[float] = Field(
        default=None,
        title="Normalized Power",
        description="Normalized power estimate for the activity in watts.",
    )

    avgVerticalOscillation: Optional[float] = Field(
        default=None,
        title="Average Vertical Oscillation",
        description="Average vertical oscillation during the activity in centimeters.",
    )

    avgGroundContactTime: Optional[float] = Field(
        default=None,
        title="Average Ground Contact Time",
        description="Average ground contact time during the activity in milliseconds.",
    )

    avgStrideLength: Optional[float] = Field(
        default=None,
        title="Average Stride Length",
        description="Average stride length during the activity in centimeters.",
    )

    vO2MaxValue: Optional[float] = Field(
        default=None,
        title="VO2 Max Value",
        description="VO2 max estimate associated with the activity.",
    )

    avgVerticalRatio: Optional[float] = Field(
        default=None,
        title="Average Vertical Ratio",
        description="Average vertical ratio during the activity.",
    )

    workoutId: Optional[int] = Field(
        default=None,
        title="Workout ID",
        description="Identifier of the associated Garmin workout, if any.",
    )

    deviceId: Optional[int] = Field(
        default=None,
        title="Device ID",
        description="Identifier of the Garmin device that recorded the activity.",
    )

    minTemperature: Optional[float] = Field(
        default=None,
        title="Minimum Temperature",
        description="Minimum recorded temperature during the activity in Celsius.",
    )

    maxTemperature: Optional[float] = Field(
        default=None,
        title="Maximum Temperature",
        description="Maximum recorded temperature during the activity in Celsius.",
    )

    minElevation: Optional[float] = Field(
        default=None,
        title="Minimum Elevation",
        description="Minimum elevation recorded during the activity in meters.",
    )

    maxElevation: Optional[float] = Field(
        default=None,
        title="Maximum Elevation",
        description="Maximum elevation recorded during the activity in meters.",
    )

    avgElevation: Optional[float] = Field(
        default=None,
        title="Average Elevation",
        description="Average elevation during the activity in meters.",
    )

    maxDoubleCadence: Optional[float] = Field(
        default=None,
        title="Max Double Cadence",
        description="Maximum double cadence value recorded during the activity.",
    )

    lapCount: Optional[int] = Field(
        default=None,
        title="Lap Count",
        description="Number of laps recorded for the activity.",
    )

    locationName: Optional[str] = Field(
        default=None,
        title="Location Name",
        description="Human-readable location associated with the activity.",
    )

    startLatitude: Optional[float] = Field(
        default=None,
        title="Start Latitude",
        description="Latitude of the activity start point.",
    )

    startLongitude: Optional[float] = Field(
        default=None,
        title="Start Longitude",
        description="Longitude of the activity start point.",
    )

    endLatitude: Optional[float] = Field(
        default=None,
        title="End Latitude",
        description="Latitude of the activity end point.",
    )

    endLongitude: Optional[float] = Field(
        default=None,
        title="End Longitude",
        description="Longitude of the activity end point.",
    )

    waterEstimated: Optional[float] = Field(
        default=None,
        title="Water Estimated",
        description="Estimated water loss for the activity.",
    )

    trainingEffectLabel: Optional[str] = Field(
        default=None,
        title="Training Effect Label",
        description="Garmin categorical label for training effect.",
    )

    activityTrainingLoad: Optional[float] = Field(
        default=None,
        title="Activity Training Load",
        description="Training load score assigned to the activity.",
    )

    aerobicTrainingEffectMessage: Optional[str] = Field(
        default=None,
        title="Aerobic Training Effect Message",
        description="Garmin message describing aerobic training effect.",
    )

    anaerobicTrainingEffectMessage: Optional[str] = Field(
        default=None,
        title="Anaerobic Training Effect Message",
        description="Garmin message describing anaerobic training effect.",
    )

    moderateIntensityMinutes: Optional[int] = Field(
        default=None,
        title="Moderate Intensity Minutes",
        description="Minutes spent in moderate intensity during the activity.",
    )

    vigorousIntensityMinutes: Optional[int] = Field(
        default=None,
        title="Vigorous Intensity Minutes",
        description="Minutes spent in vigorous intensity during the activity.",
    )

    differenceBodyBattery: Optional[int] = Field(
        default=None,
        title="Difference Body Battery",
        description="Net change in Body Battery during the activity.",
    )

    activityUUID: Optional[Any] = Field(
        default=None,
        title="Activity UUID",
        description="Globally unique identifier of the activity (string or nested uuid object).",
    )

    purposeful: Optional[bool] = Field(
        default=None,
        title="Purposeful",
        description="Whether Garmin marks this activity as purposeful.",
    )

    pr: Optional[bool] = Field(
        default=None,
        title="PR",
        description="Whether the activity includes a personal record.",
    )

    activityType: Optional[ActivityTypeSchema] = None
