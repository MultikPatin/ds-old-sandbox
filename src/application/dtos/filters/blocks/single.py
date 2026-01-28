from abgroup_core.dtos.pagination import (
    CursorParamsDTO,
    LimitOffsetParamsDTO,
    PagesParamsDTO,
)
from pydantic import BaseModel


class _LayoutSingleFilters(BaseModel):
    pass


class LayoutSinglePagesFilters(
    _LayoutSingleFilters,
    PagesParamsDTO,
):
    pass


class LayoutSingleLimitOffsetFilters(
    _LayoutSingleFilters,
    LimitOffsetParamsDTO,
):
    pass


class LayoutSingleCursorFilters(
    _LayoutSingleFilters,
    CursorParamsDTO,
):
    pass
