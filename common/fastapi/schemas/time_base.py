from datetime import date, datetime, time

from pydantic import BaseModel, Field

from .descriptions import (
    DATE_PYDANTIC_FIELD_DESCRIPTION,
    DATE_PYDANTIC_FIELD_EXAMPLES,
    DATETIME_PYDANTIC_FIELD_DESCRIPTION,
    DATETIME_PYDANTIC_FIELD_EXAMPLES,
    TIME_PYDANTIC_FIELD_DESCRIPTION,
    TIME_PYDANTIC_FIELD_EXAMPLES,
)


class CreatedSchema(BaseModel):
    created: datetime = Field(
        alias="created",
        title="Entity creation date",
        description="Entity creation date",
        examples=["2024-04-19T17:17:31.711Z"],
    )


class UpdatedSchema(BaseModel):
    updated: datetime = Field(
        alias="updated",
        title="Entity update date",
        description="Entity update date",
        examples=["2024-04-19T17:17:31.711Z"],
    )


class DateTimeStartSchema(BaseModel):
    period_start: datetime | None = Field(
        default=None,
        alias="period_start",
        title="Selection period start date and time",
        description=f"Selection period start date and time <br><br>"
        f"{DATETIME_PYDANTIC_FIELD_DESCRIPTION}",
        examples=DATETIME_PYDANTIC_FIELD_EXAMPLES,
    )


class DateTimeEndSchema(BaseModel):
    period_end: datetime | None = Field(
        default=None,
        alias="period_end",
        title="Selection period end date and time",
        description=f"Selection period end date and time <br><br>"
        f"{DATETIME_PYDANTIC_FIELD_DESCRIPTION}",
        examples=DATETIME_PYDANTIC_FIELD_EXAMPLES,
    )


class DateStartSchema(BaseModel):
    period_start: date | None = Field(
        default=None,
        alias="period_start",
        title="Selection period start date",
        description=f"Selection period start date <br><br>"
        f"{DATE_PYDANTIC_FIELD_DESCRIPTION}",
        examples=DATE_PYDANTIC_FIELD_EXAMPLES,
    )


class DateEndSchema(BaseModel):
    period_end: date | None = Field(
        default=None,
        alias="period_end",
        title="Selection period end date",
        description=f"Selection period end date <br><br>"
        f"{DATE_PYDANTIC_FIELD_DESCRIPTION}",
        examples=DATE_PYDANTIC_FIELD_EXAMPLES,
    )


class TimeStartSchema(BaseModel):
    period_start: time | None = Field(
        default=None,
        alias="period_start",
        title="Selection period start time",
        description=f"Selection period start time <br><br>"
        f"{TIME_PYDANTIC_FIELD_DESCRIPTION}",
        examples=TIME_PYDANTIC_FIELD_EXAMPLES,
    )


class TimeEndSchema(BaseModel):
    period_end: time | None = Field(
        default=None,
        alias="period_end",
        title="Selection period end time",
        description=f"Selection period end time <br><br>"
        f"{TIME_PYDANTIC_FIELD_DESCRIPTION}",
        examples=TIME_PYDANTIC_FIELD_EXAMPLES,
    )
