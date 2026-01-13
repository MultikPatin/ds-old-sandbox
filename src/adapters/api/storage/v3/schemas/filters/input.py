from abgroup_fastapi.schemas import (
    DateTimeEndSchema,
    DateTimeStartSchema,
    LifeActionSortOrNoneSchema,
    LifeActionsPeriodFieldSchema,
    LifeStatusOrNoneSchema,
)
from abgroup_fastapi.schemas.pagination import (
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
    layout_key: str = Field(
        alias="layout_key",
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
