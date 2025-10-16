from pydantic import BaseModel, Field

from common.core.enums import (
    CreateUpdateEnum,
    LifeActionTimeSortEnum,
    LifeStatusEnum,
)


class LifeStatusOrNoneSchema(BaseModel):
    status: LifeStatusEnum | None = Field(
        default=None,
        alias="status",
        title="Life status",
        description="Entity life status <br><br>",
    )


class LifeStatusSchema(BaseModel):
    status: LifeStatusEnum = Field(
        alias="status",
        title="Life status",
        description="Entity life status <br><br>",
    )


class LifeActionSortOrNoneSchema(BaseModel):
    life_time_sort: LifeActionTimeSortEnum | None = Field(
        default=None,
        alias="life_time_sort",
        title="Life status sort",
        description="Sorting by action of the entity's lifecycle <br><br>",
    )


class LifeActionSortSchema(BaseModel):
    life_time_sort: LifeActionTimeSortEnum | None = Field(
        alias="life_time_sort",
        title="Life status sort",
        description="Sorting by action of the entity's lifecycle <br><br>",
    )


class LifeActionsPeriodFieldSchema(BaseModel):
    life_action_field: CreateUpdateEnum = Field(
        alias="life_action_field",
        default=CreateUpdateEnum.created,
        title="Life action name",
        description="Life action name for filtering the sample period <br><br>",
        examples=list(CreateUpdateEnum),
    )
