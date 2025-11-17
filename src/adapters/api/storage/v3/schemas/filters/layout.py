from common.fastapi.schemas.pagination import (
    CursorParams,
    LimitOffsetParams,
    PagesParams,
)
from pydantic import BaseModel, Field


class LayoutFiltersRequest(BaseModel):
    include_schema_layer: bool = Field(
        default=True,
        alias="include_schema_layer",
        title="Is use schema layer",
        description="Include a schema layer in the response",
    )
    include_validation_layer: bool = Field(
        default=False,
        alias="include_validation_layer",
        title="Is use validation layer",
        description="Include a validation layer in the response",
    )
    include_style_layer: bool = Field(
        default=True,
        alias="include_style_layer",
        title="Is use style layer",
        description="Include a style layer in the response",
    )


class _LayoutShortFilters(BaseModel):
    pass


class LayoutShortLimitOffsetFiltersRequest(
    LimitOffsetParams,
    _LayoutShortFilters,
):
    pass


class LayoutShortPagesFiltersRequest(
    PagesParams,
    _LayoutShortFilters,
):
    pass


class LayoutShortCursorFiltersRequest(
    CursorParams,
    _LayoutShortFilters,
):
    pass
