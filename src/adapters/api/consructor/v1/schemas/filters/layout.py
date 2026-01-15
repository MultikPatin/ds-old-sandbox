from abgroup_fastapi.schemas.pagination import (
    CursorParams,
    LimitOffsetParams,
    PagesParams,
)
from pydantic import BaseModel

# ===========


class _LayoutMassagePaginationFilters(BaseModel):
    pass


class LayoutMessageLimitOffsetFiltersRequest(
    LimitOffsetParams,
    _LayoutMassagePaginationFilters,
):
    pass


class LayoutMessagePagesFiltersRequest(
    PagesParams,
    _LayoutMassagePaginationFilters,
):
    pass


class LayoutMessageCursorFiltersRequest(
    CursorParams,
    _LayoutMassagePaginationFilters,
):
    pass


# ===========


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


# ===========


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
    _LayoutMassagePaginationFilters,
):
    pass
