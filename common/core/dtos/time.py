from datetime import datetime

from pydantic import BaseModel, Field

from common.core.constants import DEFAULT_DELETED_AT_DATETIME
from common.core.utils import time_now


class UseUntilDTO(BaseModel):
    used_until: datetime = Field(default=DEFAULT_DELETED_AT_DATETIME)


class CreatedDTO(BaseModel):
    created: datetime = Field(default_factory=time_now)


class UpdatedDTO(BaseModel):
    updated: datetime = Field(default_factory=time_now)


class DateTimeStartDTO(BaseModel):
    period_start: datetime | None = Field(default=None)


class DateTimeEndDTO(BaseModel):
    period_end: datetime | None = Field(default=None)


class DateStartDTO(BaseModel):
    period_start: datetime | None = Field(default=None)


class DateEndDTO(BaseModel):
    period_end: datetime | None = Field(default=None)


class TimeStartDTO(BaseModel):
    period_start: datetime | None = Field(default=None)


class TimeEndDTO(BaseModel):
    period_end: datetime | None = Field(default=None)
