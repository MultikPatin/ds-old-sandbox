from collections.abc import Set

from abgroup_core.dtos.pagination import (
    CursorParamsDTO,
    LimitOffsetParamsDTO,
    PagesParamsDTO,
)
from abgroup_core.enums import LifeStatusEnum
from pydantic import BaseModel, Field

from src.application.enums import LayoutBlocksEnum, LayoutLayersEnum


class LayersFetcherFilters(BaseModel):
    layers: Set[LayoutLayersEnum] = Field(default_factory=set)


class BlocksFetcherFilters(BaseModel):
    blocks: Set[LayoutBlocksEnum] = Field(default_factory=set)


class LayoutFetcherFilters(
    LayersFetcherFilters,
    BlocksFetcherFilters,
):
    pass


# ==========


class _LayoutShortFilters(BaseModel):
    status: LifeStatusEnum | None = Field(default=LifeStatusEnum.published)


class LayoutShortPagesFilters(
    _LayoutShortFilters,
    PagesParamsDTO,
):
    pass


class LayoutShortLimitOffsetFilters(
    _LayoutShortFilters,
    LimitOffsetParamsDTO,
):
    pass


class LayoutShortCursorFilters(
    _LayoutShortFilters,
    CursorParamsDTO,
):
    pass
