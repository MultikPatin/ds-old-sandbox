from collections.abc import Iterable, MutableSequence

from src.application.enums import LayoutBlocksEnum, LayoutLayersEnum

from .helpers import (
    _BLOCKS_TYPE,
    _EXTRACTION_ERROR_GROUP_MSG,
    _INVALID_TYPE_MSG,
    _Block,
    _BlockGroup,
    _BlocksNames,
    _IDsByLayers,
    _LayerIds,
    _LayersNames,
    _Layout,
)


def _collect_layer_ids(
    blocks: Iterable[_Block], layers: _LayersNames
) -> _IDsByLayers:
    result: _IDsByLayers = {x: set() for x in layers}

    for block in blocks:
        layers_map = _extract_layers_ids(block, layers)
        for layer, ids in layers_map.items():
            if ids:
                result[layer].update(ids)

    return result


def _collect_blocks(layout: _Layout, blocks: _BlocksNames) -> list[_Block]:
    errors = []
    results: list[_Block] = []

    for block in blocks:
        try:
            group = _extract_group(layout, block)
            if group is not None:
                results.extend(group)
        except TypeError as e:
            errors.append(e)

    if errors:
        raise ExceptionGroup(_EXTRACTION_ERROR_GROUP_MSG, errors)

    return results


def _extract_group(layout: _Layout, block: LayoutBlocksEnum) -> _BlockGroup:
    attr = layout.get(block)

    if attr is None:
        return attr

    if not isinstance(attr, MutableSequence):
        raise TypeError(
            _INVALID_TYPE_MSG.format(
                name=block.value,
                valid_types=_BLOCKS_TYPE,
                acc_type=type(attr),
            )
        )

    return attr


def _extract_layers_ids(block: _Block, layers: _LayersNames) -> _IDsByLayers:
    errors = []
    results = {}

    for layer in layers:
        try:
            ids = _extract_layer_ids(block, layer)
            if ids:
                results[layer] = ids
        except TypeError as e:
            errors.append(e)

    if errors:
        raise ExceptionGroup(_EXTRACTION_ERROR_GROUP_MSG, errors)

    return results


def _extract_layer_ids(block: _Block, layer: LayoutLayersEnum) -> set[str]:
    attr = block.get(layer)

    if attr is None:
        return set()

    if not isinstance(attr, MutableSequence):
        raise TypeError(
            _INVALID_TYPE_MSG.format(
                name=layer.value,
                valid_types=_BLOCKS_TYPE,
                acc_type=type(attr),
            )
        )

    return _extract_ids(attr, layer)


def _extract_ids(ids: _LayerIds, layer: LayoutLayersEnum) -> set[str]:
    result: set[str] = set()

    for i in ids:
        if isinstance(i, MutableSequence):
            result.update(_extract_ids(i, layer))
        elif isinstance(i, str):
            result.add(i)
        elif i is None:
            continue
        else:
            raise TypeError(
                _INVALID_TYPE_MSG.format(
                    name=layer.value,
                    valid_types=_BLOCKS_TYPE,
                    acc_type=type(i),
                )
            )

    return result
