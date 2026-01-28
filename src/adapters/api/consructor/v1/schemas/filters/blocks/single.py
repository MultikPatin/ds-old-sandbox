from abgroup_fastapi.schemas.pagination import (
    CursorParams,
    LimitOffsetParams,
    PagesParams,
)
from pydantic import BaseModel


class _LayoutSinglePaginationFilters(BaseModel):
    pass


class LayoutSingleLimitOffsetFiltersRequest(
    LimitOffsetParams,
    _LayoutSinglePaginationFilters,
):
    pass


class LayoutSinglePagesFiltersRequest(
    PagesParams,
    _LayoutSinglePaginationFilters,
):
    pass


class LayoutSingleCursorFiltersRequest(
    CursorParams,
    _LayoutSinglePaginationFilters,
):
    pass
