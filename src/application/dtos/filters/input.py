from common.core.dtos import (
    DateTimeEndDTO,
    DateTimeStartDTO,
    LifeActionsPeriodFieldDTO,
    LifeActionTimeSortOrNoneDTO,
    LifeStatusOrNoneDTO,
)
from common.core.dtos.pagination import (
    CursorParamsDTO,
    LimitOffsetParamsDTO,
    PagesParamsDTO,
)
from pydantic import Field


class InputCardFilters(
    DateTimeStartDTO,
    DateTimeEndDTO,
    LifeActionsPeriodFieldDTO,
    LifeStatusOrNoneDTO,
    LifeActionTimeSortOrNoneDTO,
):
    layout_ids: list[str] = Field(default_factory=list)
    layouts_key: str = Field(min_length=1)


class InputCardPagesFilters(InputCardFilters, PagesParamsDTO):
    pass


class InputCardLimitOffsetFilters(InputCardFilters, LimitOffsetParamsDTO):
    pass


class InputCardCursorFilters(InputCardFilters, CursorParamsDTO):
    pass
