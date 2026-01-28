from collections.abc import Set

from pydantic import BaseModel, Field, computed_field

from src.application.enums import LayoutBlocksEnum, LayoutLayersEnum


class LayersFetcherFiltersRequest(BaseModel):
    include_schema_layer: bool = Field(
        default=True,
        alias="include_schema_layer",
        title="Using schema layer",
        description="Include a schema layer in the response",
        exclude=True,
    )
    include_validation_layer: bool = Field(
        default=True,
        alias="include_validation_layer",
        title="Using validation layer",
        description="Include a validation layer in the response",
        exclude=True,
    )
    include_style_layer: bool = Field(
        default=True,
        alias="include_style_layer",
        title="Using style layer",
        description="Include a style layer in the response",
        exclude=True,
    )
    include_default_layer: bool = Field(
        default=True,
        alias="include_default_layer",
        title="Using default layer",
        description="Include a default layer in the response",
        exclude=True,
    )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def layers(self) -> Set[LayoutLayersEnum]:
        result = set()

        if self.include_schema_layer:
            result.add(LayoutLayersEnum.schemas)
        if self.include_style_layer:
            result.add(LayoutLayersEnum.styles)
        if self.include_validation_layer:
            result.add(LayoutLayersEnum.validations)
        if self.include_default_layer:
            result.add(LayoutLayersEnum.defaults)

        return result


class BlocksFetcherFiltersRequest(BaseModel):
    include_single_block: bool = Field(
        default=True,
        alias="include_single_block",
        title="Using single block",
        description="Include a single block in the response",
        exclude=True,
    )
    include_table_block: bool = Field(
        default=True,
        alias="include_table_block",
        title="Using table block",
        description="Include a table block in the response",
        exclude=True,
    )
    include_message_block: bool = Field(
        default=True,
        alias="include_message_block",
        title="Using message block",
        description="Include a message block in the response",
        exclude=True,
    )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def blocks(self) -> Set[LayoutBlocksEnum]:
        result = set()

        if self.include_single_block:
            result.add(LayoutBlocksEnum.singles)
        if self.include_table_block:
            result.add(LayoutBlocksEnum.tables)
        if self.include_message_block:
            result.add(LayoutBlocksEnum.messages)

        return result


class LayoutFetcherFiltersRequest(
    LayersFetcherFiltersRequest,
    BlocksFetcherFiltersRequest,
):
    pass
