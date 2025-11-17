from common.fastapi.schemas import (
    DateTimeEndSchema,
    DateTimeStartSchema,
    LifeActionSortOrNoneSchema,
    LifeActionsPeriodFieldSchema,
    LifeStatusOrNoneSchema,
)
from common.fastapi.schemas.pagination import (
    CursorParams,
    LimitOffsetParams,
    PagesParams,
)
from pydantic import Field


class _InputCardFilters(
    DateTimeStartSchema,
    DateTimeEndSchema,
    LifeActionsPeriodFieldSchema,
    LifeStatusOrNoneSchema,
    LifeActionSortOrNoneSchema,
):
    layouts_key: str = Field(
        alias="layouts_key",
        title="Layouts key",
        description="Key of layouts",
        min_length=1,
    )


class InputCardLimitOffsetFiltersRequest(
    LimitOffsetParams,
    _InputCardFilters,
):
    pass


class InputCardPagesFiltersRequest(
    PagesParams,
    _InputCardFilters,
):
    pass


class InputCardCursorFiltersRequest(
    CursorParams,
    _InputCardFilters,
):
    pass
