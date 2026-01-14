from abgroup_fastapi.schemas.pagination import (
    CursorParams,
    LimitOffsetParams,
    PagesParams,
)
from pydantic import BaseModel


class _LayoutMassagePaginationFilters(BaseModel):
    pass


class LayoutMassageLimitOffsetFiltersRequest(
    LimitOffsetParams,
    _LayoutMassagePaginationFilters,
):
    pass


class LayoutMassagePagesFiltersRequest(
    PagesParams,
    _LayoutMassagePaginationFilters,
):
    pass


class LayoutMassageCursorFiltersRequest(
    CursorParams,
    _LayoutMassagePaginationFilters,
):
    pass
