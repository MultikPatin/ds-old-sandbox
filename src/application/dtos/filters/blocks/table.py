from abgroup_core.dtos.pagination import (
    CursorParamsDTO,
    LimitOffsetParamsDTO,
    PagesParamsDTO,
)
from pydantic import BaseModel


class _LayoutTableFilters(BaseModel):
    pass


class LayoutTablePagesFilters(
    _LayoutTableFilters,
    PagesParamsDTO,
):
    pass


class LayoutTableLimitOffsetFilters(
    _LayoutTableFilters,
    LimitOffsetParamsDTO,
):
    pass


class LayoutTableCursorFilters(
    _LayoutTableFilters,
    CursorParamsDTO,
):
    pass
