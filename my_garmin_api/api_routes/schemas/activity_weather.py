"""Activity weather schema models."""

from typing import Optional

from pydantic import BaseModel, Field


class WeatherStationSchema(BaseModel):
    """Weather station metadata associated with an activity weather record."""

    id: Optional[str] = Field(
        default=None,
        title="Station ID",
        description="Provider-specific station identifier.",
    )

    name: Optional[str] = Field(
        default=None,
        title="Station Name",
        description="Human-readable station name.",
    )

    timezone: Optional[str] = Field(
        default=None,
        title="Station Timezone",
        description="IANA timezone for the station when provided.",
    )


class WeatherTypeSchema(BaseModel):
    """Describes the high-level weather classification during the activity."""

    weatherTypePk: Optional[int] = Field(
        default=None,
        title="Weather Type PK",
        description="Garmin weather type identifier if available.",
    )

    desc: Optional[str] = Field(
        default=None,
        title="Weather Description",
        description="Text weather description such as Clear or Rain.",
    )

    image: Optional[str] = Field(
        default=None,
        title="Weather Image",
        description="Optional weather icon/image reference.",
    )


class ActivityWeatherSchema(BaseModel):
    """Weather conditions near activity start time."""

    issueDate: Optional[str] = Field(
        default=None,
        title="Issue Date",
        description="Weather timestamp in ISO 8601 format.",
    )

    temp: Optional[float] = Field(
        default=None,
        title="Temperature",
        description="Measured ambient temperature.",
    )

    apparentTemp: Optional[float] = Field(
        default=None,
        title="Apparent Temperature",
        description="Feels-like temperature value.",
    )

    dewPoint: Optional[float] = Field(
        default=None,
        title="Dew Point",
        description="Dew point temperature.",
    )

    relativeHumidity: Optional[float] = Field(
        default=None,
        title="Relative Humidity",
        description="Relative humidity percentage.",
    )

    windDirection: Optional[float] = Field(
        default=None,
        title="Wind Direction",
        description="Wind direction in degrees.",
    )

    windDirectionCompassPoint: Optional[str] = Field(
        default=None,
        title="Wind Direction Compass Point",
        description="Cardinal or inter-cardinal wind direction string.",
    )

    windSpeed: Optional[float] = Field(
        default=None,
        title="Wind Speed",
        description="Sustained wind speed.",
    )

    windGust: Optional[float] = Field(
        default=None,
        title="Wind Gust",
        description="Wind gust speed when available.",
    )

    latitude: Optional[float] = Field(
        default=None,
        title="Latitude",
        description="Latitude of weather observation point.",
    )

    longitude: Optional[float] = Field(
        default=None,
        title="Longitude",
        description="Longitude of weather observation point.",
    )

    weatherStationDTO: Optional[WeatherStationSchema] = Field(
        default=None,
        title="Weather Station",
        description="Source weather station metadata.",
    )

    weatherTypeDTO: Optional[WeatherTypeSchema] = Field(
        default=None,
        title="Weather Type",
        description="Weather condition classification.",
    )
