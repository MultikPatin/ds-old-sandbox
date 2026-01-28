from collections.abc import Iterable, MutableSequence

from src.application.enums import LayoutBlocksEnum, LayoutLayersEnum

from .helpers import (
    _BLOCKS_TYPE,
    _ENTITY_HAS_NOT_BLOCK_KEYS_MSG,
    _ENTITY_HAS_NOT_ID_KEY_MSG,
    _INVALID_TYPE_MSG,
    _Block,
    _BlocksNames,
    _FetchedLayer,
    _FetchedLayersMap,
    _LayerIds,
    _Layout,
)


def _replace_layout(
    layout: _Layout, blocks: _BlocksNames, layers_map: _FetchedLayersMap
) -> None:
    missing = blocks - layout.keys()
    if missing:
        raise KeyError(
            _ENTITY_HAS_NOT_BLOCK_KEYS_MSG.format(
                missing=missing,
                blocks_names=blocks,
            )
        )

    for k in set(LayoutBlocksEnum) - blocks:
        if k in layout:
            layout[LayoutBlocksEnum(k)] = None

    for block in blocks:
        attr = layout[block]

        if attr is None:
            continue

        if not isinstance(attr, MutableSequence):
            raise TypeError(
                _INVALID_TYPE_MSG.format(
                    name=block.value,
                    valid_types=_BLOCKS_TYPE,
                    acc_type=type(attr),
                )
            )

        _replace_blocks(attr, layers_map)


def _replace_blocks(
    blocks: Iterable[_Block], layers_map: _FetchedLayersMap
) -> None:
    for block in blocks:
        intersection = block.keys() & set(LayoutLayersEnum)

        if not intersection:
            # Блок не содержит слоев
            continue

        _replace_block(block, layers_map)


def _replace_block(block: _Block, layers_map: _FetchedLayersMap) -> None:
    missing = layers_map.keys() - block.keys()
    if missing:
        raise KeyError(
            _ENTITY_HAS_NOT_BLOCK_KEYS_MSG.format(
                missing=missing,
                blocks_names=layers_map.keys(),
            )
        )

    for k in set(LayoutLayersEnum) - layers_map.keys():
        if k in block:
            block[LayoutLayersEnum(k)] = None

    for k, v in layers_map.items():
        attr = block[k]
        if not attr:
            continue
        _replace_layer(attr, v)


def _replace_layer(layer: _LayerIds, layers_map: _FetchedLayer) -> None:
    if not isinstance(layer[0], MutableSequence):
        _replace_layer_helper(layer, layers_map)
    else:
        for sublist in layer:
            if isinstance(sublist, MutableSequence):
                _replace_layer_helper(sublist, layers_map)


def _replace_layer_helper(layer: _LayerIds, layers_map: _FetchedLayer) -> None:
    for i in range(len(layer)):
        k = layer[i]
        if k is None:
            continue
        if k in layers_map and isinstance(k, str):
            layer[i] = layers_map[k]
        else:
            raise KeyError(_ENTITY_HAS_NOT_ID_KEY_MSG.format(id_list=k))
