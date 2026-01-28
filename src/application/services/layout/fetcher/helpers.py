from collections.abc import (
    Iterable,
    Mapping,
    MutableMapping,
    MutableSequence,
    Set,
)
from typing import Any

from src.application.enums import LayoutBlocksEnum, LayoutLayersEnum

type _LayersNames = Set[LayoutLayersEnum]
type _LayerIds = MutableSequence[str] | MutableSequence[MutableSequence[str]]
type _IDsByLayers = Mapping[LayoutLayersEnum, set[str]]

type _FetchedLayer = Mapping[str, Any]
type _FetchedLayersMap = Mapping[LayoutLayersEnum, _FetchedLayer]

type _BlocksNames = Set[LayoutBlocksEnum]
type _Block = MutableMapping[LayoutLayersEnum, _LayerIds | None]
type _BlockGroup = Iterable[_Block] | None

type _Layout = MutableMapping[LayoutBlocksEnum, Iterable[_Block] | None]


_BLOCKS_TYPE = (None, MutableSequence[Any])


_EXTRACTION_ERROR_GROUP_MSG = "Error occurred while extracting"

_INVALID_TYPE_MSG = (
    "Attribute '{name}' type must be one of: '{valid_types}', "
    "but got: '{acc_type}'"
)

_ENTITY_HAS_NOT_BLOCK_KEYS_MSG = (
    "The entity does not contain the keys '{missing}' "
    "from the expected set '{blocks_names}'"
)
_ENTITY_HAS_NOT_ID_KEY_MSG = (
    "the schema contains an id: '{id_list}' "
    "that is not present in the to_change dictionary"
)
