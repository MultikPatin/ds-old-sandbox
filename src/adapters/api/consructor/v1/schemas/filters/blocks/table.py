from abgroup_fastapi.schemas.pagination import (
    CursorParams,
    LimitOffsetParams,
    PagesParams,
)
from pydantic import BaseModel


class _LayoutTablePaginationFilters(BaseModel):
    pass


class LayoutTableLimitOffsetFiltersRequest(
    LimitOffsetParams,
    _LayoutTablePaginationFilters,
):
    pass


class LayoutTablePagesFiltersRequest(
    PagesParams,
    _LayoutTablePaginationFilters,
):
    pass


class LayoutTableCursorFiltersRequest(
    CursorParams,
    _LayoutTablePaginationFilters,
):
    pass
