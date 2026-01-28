from abgroup_core.dtos.pagination import (
    CursorParamsDTO,
    LimitOffsetParamsDTO,
    PagesParamsDTO,
)
from pydantic import BaseModel


class _LayoutMessageFilters(BaseModel):
    pass


class LayoutMessagePagesFilters(
    _LayoutMessageFilters,
    PagesParamsDTO,
):
    pass


class LayoutMessageLimitOffsetFilters(
    _LayoutMessageFilters,
    LimitOffsetParamsDTO,
):
    pass


class LayoutMessageCursorFilters(
    _LayoutMessageFilters,
    CursorParamsDTO,
):
    pass
