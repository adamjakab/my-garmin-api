"""Activity gear schema models."""

from typing import Optional

from pydantic import BaseModel, Field


class ActivityGearSchema(BaseModel):
    """Gear metadata associated with an activity."""

    gearPk: Optional[int] = Field(
        default=None,
        title="Gear PK",
        description="Unique Garmin gear identifier.",
    )

    uuid: Optional[str] = Field(
        default=None,
        title="Gear UUID",
        description="Persistent UUID for the gear item.",
    )

    userProfilePk: Optional[int] = Field(
        default=None,
        title="User Profile PK",
        description="Owner profile identifier for the gear.",
    )

    gearMakeName: Optional[str] = Field(
        default=None,
        title="Gear Make Name",
        description="Manufacturer or make name.",
    )

    gearModelName: Optional[str] = Field(
        default=None,
        title="Gear Model Name",
        description="Model name reported by Garmin.",
    )

    gearTypeName: Optional[str] = Field(
        default=None,
        title="Gear Type Name",
        description="Gear category such as Shoes.",
    )

    gearStatusName: Optional[str] = Field(
        default=None,
        title="Gear Status Name",
        description="Lifecycle status such as active or retired.",
    )

    displayName: Optional[str] = Field(
        default=None,
        title="Display Name",
        description="User-facing short display label.",
    )

    customMakeModel: Optional[str] = Field(
        default=None,
        title="Custom Make Model",
        description="Custom gear make/model text provided by the user.",
    )

    imageNameLarge: Optional[str] = Field(
        default=None,
        title="Image Name Large",
        description="Large image asset name when provided.",
    )

    imageNameMedium: Optional[str] = Field(
        default=None,
        title="Image Name Medium",
        description="Medium image asset name when provided.",
    )

    imageNameSmall: Optional[str] = Field(
        default=None,
        title="Image Name Small",
        description="Small image asset name when provided.",
    )

    dateBegin: Optional[str] = Field(
        default=None,
        title="Date Begin",
        description="Gear start date in ISO 8601 format.",
    )

    dateEnd: Optional[str] = Field(
        default=None,
        title="Date End",
        description="Gear end date in ISO 8601 format when retired.",
    )

    maximumMeters: Optional[float] = Field(
        default=None,
        title="Maximum Meters",
        description="Configured maximum distance for the gear lifecycle in meters.",
    )

    notified: Optional[bool] = Field(
        default=None,
        title="Notified",
        description="Whether the user has been notified about lifecycle threshold.",
    )

    createDate: Optional[str] = Field(
        default=None,
        title="Create Date",
        description="Gear record creation timestamp in ISO 8601 format.",
    )

    updateDate: Optional[str] = Field(
        default=None,
        title="Update Date",
        description="Last gear record update timestamp in ISO 8601 format.",
    )
