from common.core.dtos import (
    DateTimeEndDTO,
    DateTimeStartDTO,
    LifeActionsPeriodFieldDTO,
    LifeActionTimeSortOrNoneDTO,
    LifeStatusOrNoneDTO,
)
from pydantic import Field


class InputCardFilters(
    LifeActionTimeSortOrNoneDTO,
    LifeStatusOrNoneDTO,
    DateTimeStartDTO,
    DateTimeEndDTO,
    LifeActionsPeriodFieldDTO,
):
    model_id: str
    layout_ids: list[str] = Field(default_factory=list)
