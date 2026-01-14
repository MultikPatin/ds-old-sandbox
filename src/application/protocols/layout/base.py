from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from src.application.enums import LayoutLayersEnum


class LayersFiltersProtocol(Protocol):
    include_schema_layer: bool
    include_validation_layer: bool
    include_style_layer: bool
    include_default_layer: bool

    @property
    def excluded_layers(self) -> tuple["LayoutLayersEnum", ...]: ...
