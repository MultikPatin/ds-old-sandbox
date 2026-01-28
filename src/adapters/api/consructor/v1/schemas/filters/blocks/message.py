from abgroup_fastapi.schemas.pagination import (
    CursorParams,
    LimitOffsetParams,
    PagesParams,
)
from pydantic import BaseModel


class _LayoutMessagePaginationFilters(BaseModel):
    pass


class LayoutMessageLimitOffsetFiltersRequest(
    LimitOffsetParams,
    _LayoutMessagePaginationFilters,
):
    pass


class LayoutMessagePagesFiltersRequest(
    PagesParams,
    _LayoutMessagePaginationFilters,
):
    pass


class LayoutMessageCursorFiltersRequest(
    CursorParams,
    _LayoutMessagePaginationFilters,
):
    pass
