from abgroup_core.dtos.pagination import (
    CursorParamsDTO,
    LimitOffsetParamsDTO,
    PagesParamsDTO,
)
from abgroup_core.enums import LifeStatusEnum
from pydantic import BaseModel, Field

from src.application.enums import LayoutLayersEnum


class LayoutFilters(BaseModel):
    include_schema_layer: bool = Field(default=True)
    include_validation_layer: bool = Field(default=False)
    include_style_layer: bool = Field(default=True)
    include_default_layer: bool = Field(default=False)

    @property
    def excluded_layers(self) -> tuple[LayoutLayersEnum, ...]:
        exclude: list[LayoutLayersEnum] = []
        if not self.include_schema_layer:
            exclude.append(LayoutLayersEnum.schemas)
        if not self.include_style_layer:
            exclude.append(LayoutLayersEnum.styles)
        if not self.include_validation_layer:
            exclude.append(LayoutLayersEnum.validations)
        if not self.include_default_layer:
            exclude.append(LayoutLayersEnum.defaults)

        return tuple(exclude)

    # @property
    # def excluded_blocks(self) -> tuple[LayoutBlocksEnum, ...]:
    #     exclude: list[LayoutBlocksEnum] = []
    #     return tuple(exclude)


class LayoutShortFilters(BaseModel):
    status: LifeStatusEnum | None = Field(default=LifeStatusEnum.published)


class LayoutShortPagesFilters(LayoutShortFilters, PagesParamsDTO):
    pass


class LayoutShortLimitOffsetFilters(LayoutShortFilters, LimitOffsetParamsDTO):
    pass


class LayoutShortCursorFilters(LayoutShortFilters, CursorParamsDTO):
    pass
