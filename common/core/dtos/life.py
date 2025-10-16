from pydantic import BaseModel, Field

from common.core.enums import (
    CreateUpdateEnum,
    LifeActionTimeSortEnum,
    LifeStatusEnum,
)


class LifeStatusDTO(BaseModel):
    status: LifeStatusEnum = Field(default=LifeStatusEnum.created)


class LifeStatusOrNoneDTO(BaseModel):
    status: LifeStatusEnum | None = Field(default=None)


class LifeActionTimeSortOrNoneDTO(BaseModel):
    live_time_sort: LifeActionTimeSortEnum | None = Field(default=None)


class LifeActionsPeriodFieldDTO(BaseModel):
    life_action_field: CreateUpdateEnum
