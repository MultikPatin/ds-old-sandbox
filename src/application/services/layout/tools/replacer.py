from collections.abc import (
    Iterable,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)
from itertools import chain
from typing import TYPE_CHECKING, Any

from common.core.custom_types import AnyDict

from src.application.enums import LayoutBlocksEnum, LayoutLayersEnum

if TYPE_CHECKING:
    from src.application.dtos.db import LayoutWithBlocks

type _IDsByLayers = dict[LayoutLayersEnum, set[str]]
type _Original = MutableSequence[str] | MutableSequence[MutableSequence[str]]
type _Originals = Iterable[MutableMapping[LayoutLayersEnum, _Original]]
type _Exclude = Sequence[LayoutLayersEnum] | None
type _Changes = Mapping[LayoutLayersEnum, Mapping[str, Any]]
type _Change = Mapping[str, Any]


def get_ids_by_layers(
    layout: "LayoutWithBlocks", *, exclude: _Exclude = None
) -> _IDsByLayers:
    ids: _IDsByLayers = {x: set() for x in LayoutLayersEnum.layers(exclude)}

    if layout.singles:
        for s in layout.singles:
            for k, v in ids.items():
                attr = getattr(s, k)
                if isinstance(attr, Iterable):
                    v.update(attr)

    if layout.tables:
        for t in layout.tables:
            for k, v in ids.items():
                attr = getattr(t, k)
                if isinstance(attr, Iterable):
                    v.update(chain(*attr))

    return ids


def replace_layers(layout: "LayoutWithBlocks", changes: _Changes) -> AnyDict:
    obj = layout.model_dump()

    missing = set(LayoutBlocksEnum) - obj.keys()
    if missing:
        msg = (
            f"The schema does not contain the blocks {missing} "
            f"from the expected set {set(LayoutBlocksEnum)}"
        )
        raise KeyError(msg)

    # TODO: Проверить и реализовать удаление блоков если они не нужны

    for k in LayoutBlocksEnum:
        _replace_layers_in_blocks(obj[k], changes)

    return obj


def _replace_layers_in_blocks(originals: _Originals, changes: _Changes) -> None:
    for original in originals:
        missing = changes.keys() - original.keys()
        if missing:
            msg = (
                f"The schema does not contain the keys {missing} "
                f"from the expected set {changes.keys()}"
            )
            raise KeyError(msg)

        for k in set(LayoutLayersEnum) - changes.keys():
            if k in original:
                del original[LayoutLayersEnum(k)]

        for k, v in changes.items():
            _replace_layers_in_block(original[k], v)


def _replace_layers_in_block(original: _Original, change: _Change) -> None:
    if not original:
        return

    if not isinstance(original[0], MutableSequence):
        for i in range(len(original)):
            k = original[i]
            if k in change and isinstance(k, str):
                original[i] = change[k]
            else:
                msg = (
                    f"the schema contains an id: {k} "
                    f"that is not present in the to_change dictionary"
                )
                raise KeyError(msg)
    else:
        for sublist in original:
            if isinstance(sublist, MutableSequence):
                for i in range(len(sublist)):
                    k = sublist[i]
                    if k in change:
                        sublist[i] = change[k]
                    else:
                        msg = (
                            f"the schema contains an id: {k} "
                            f"that is not present in the to_change dictionary"
                        )
                        raise KeyError(msg)
