from collections.abc import Set
from typing import Protocol

from src.application.enums import LayoutBlocksEnum, LayoutLayersEnum


class LayersFetcherFiltersProtocol(Protocol):
    layers: Set[LayoutLayersEnum]


class BlocksFetcherFiltersProtocol(Protocol):
    blocks: Set[LayoutBlocksEnum]


class LayoutFetcherFiltersProtocol(
    LayersFetcherFiltersProtocol,
    BlocksFetcherFiltersProtocol,
    Protocol,
): ...
