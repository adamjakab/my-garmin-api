"""HRV response schema models for FastAPI routes."""

from typing import Optional

from pydantic import BaseModel, Field


class HrvBaselineSchema(BaseModel):
    """Baseline thresholds used for Garmin HRV status interpretation."""

    model_config = {
        "extra": "ignore",
    }

    lowUpper: Optional[float] = Field(
        default=None,
        title="Low Upper",
        description="Upper threshold for the low HRV range.",
    )
    balancedLow: Optional[float] = Field(
        default=None,
        title="Balanced Low",
        description="Lower threshold for the balanced HRV range.",
    )
    balancedUpper: Optional[float] = Field(
        default=None,
        title="Balanced Upper",
        description="Upper threshold for the balanced HRV range.",
    )
    markerValue: Optional[float] = Field(
        default=None,
        title="Marker Value",
        description="Garmin internal marker used in HRV baseline calculation.",
    )


class HrvSummarySchema(BaseModel):
    """Summary metrics for a single night's HRV session."""

    model_config = {
        "extra": "ignore",
    }

    calendarDate: Optional[str] = Field(
        default=None,
        title="Calendar Date",
        description="Date of the HRV summary in YYYY-MM-DD format.",
    )
    weeklyAvg: Optional[float] = Field(
        default=None,
        title="Weekly Average",
        description="7-day rolling average HRV value.",
    )
    lastNightAvg: Optional[float] = Field(
        default=None,
        title="Last Night Average",
        description="Average HRV measured during the latest sleep session.",
    )
    lastNight5MinHigh: Optional[float] = Field(
        default=None,
        title="Last Night 5-Min High",
        description="Highest 5-minute HRV segment during the latest sleep session.",
    )
    baseline: Optional[HrvBaselineSchema] = Field(
        default=None,
        title="Baseline",
        description="Baseline zone thresholds used for HRV status evaluation.",
    )
    status: Optional[str] = Field(
        default=None,
        title="Status",
        description="Garmin HRV status classification (for example: BALANCED, UNBALANCED).",
    )
    feedbackPhrase: Optional[str] = Field(
        default=None,
        title="Feedback Phrase",
        description="Garmin feedback phrase identifier associated with the status.",
    )
    createTimeStamp: Optional[str] = Field(
        default=None,
        title="Created Timestamp",
        description="Timestamp when Garmin generated the HRV summary.",
    )


class HrvPayloadSchema(BaseModel):
    """HRV payload for a single date after response sanitization."""

    model_config = {
        "extra": "ignore",
    }

    userProfilePk: Optional[int] = Field(
        default=None,
        title="User Profile PK",
        description="Garmin user profile identifier.",
    )
    hrvSummary: Optional[HrvSummarySchema] = Field(
        default=None,
        title="HRV Summary",
        description="Daily HRV summary metrics and baseline interpretation.",
    )
    startTimestampGMT: Optional[str] = Field(
        default=None,
        title="Start Timestamp GMT",
        description="Start timestamp of the HRV sampling session in GMT.",
    )
    endTimestampGMT: Optional[str] = Field(
        default=None,
        title="End Timestamp GMT",
        description="End timestamp of the HRV sampling session in GMT.",
    )
    startTimestampLocal: Optional[str] = Field(
        default=None,
        title="Start Timestamp Local",
        description="Start timestamp of the HRV sampling session in local time.",
    )
    endTimestampLocal: Optional[str] = Field(
        default=None,
        title="End Timestamp Local",
        description="End timestamp of the HRV sampling session in local time.",
    )
    sleepStartTimestampGMT: Optional[str] = Field(
        default=None,
        title="Sleep Start Timestamp GMT",
        description="Garmin-estimated sleep start timestamp in GMT.",
    )
    sleepEndTimestampGMT: Optional[str] = Field(
        default=None,
        title="Sleep End Timestamp GMT",
        description="Garmin-estimated sleep end timestamp in GMT.",
    )
    sleepStartTimestampLocal: Optional[str] = Field(
        default=None,
        title="Sleep Start Timestamp Local",
        description="Garmin-estimated sleep start timestamp in local time.",
    )
    sleepEndTimestampLocal: Optional[str] = Field(
        default=None,
        title="Sleep End Timestamp Local",
        description="Garmin-estimated sleep end timestamp in local time.",
    )


class HrvEntrySchema(BaseModel):
    date: str = Field(
        title="Date",
        description="The date of the HRV payload in YYYY-MM-DD format.",
    )
    hrv: HrvPayloadSchema = Field(
        title="HRV Data",
        description="Structured Garmin HRV payload for the date (excluding raw hrvReadings samples).",
    )


class HrvResponseSchema(BaseModel):
    start_date: str = Field(
        title="Requested start date",
        description="The start date of the requested range.",
    )
    end_date: str = Field(
        title="Requested end date",
        description="The end date of the requested range.",
    )
    count: int = Field(
        title="Count",
        description="The number of HRV records returned for the selected date range.",
    )
    hrv_data: list[HrvEntrySchema]
