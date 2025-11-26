from collections.abc import (
    Iterable,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)
from typing import TYPE_CHECKING, Any

from common.core.custom_types import AnyDict, AnyList

from src.application.enums import InputBlocksEnum, InputLayersEnum

if TYPE_CHECKING:
    from src.application.dtos.db.input import InputWithBlocks


type _Chunks = MutableSequence[Mapping[InputLayersEnum, Sequence[Any]]]
type _Tables = Iterable[_TableWithChunks]
type _TableWithChunks = MutableMapping[InputLayersEnum, _Chunks]
type _Changes = Mapping[str, Any]


def get_chunk_ids(instance: "InputWithBlocks") -> set[str]:
    ids = set()

    if instance.tables:
        for table in instance.tables:
            ids.update(table.chunks)

    return ids


def replace_layers(instance: "InputWithBlocks", changes: _Changes) -> AnyDict:
    obj = instance.model_dump()

    if InputBlocksEnum.tables in obj:
        _replace_chunks(obj[InputBlocksEnum.tables], changes)

    return obj


def _replace_chunks(tables: _Tables, changes: _Changes) -> None:
    for table in tables:
        if InputLayersEnum.chunks not in table:
            msg = f"The table does not contain the key {InputLayersEnum.chunks}"
            raise KeyError(msg)
        _replace_chunks_in_block(table[InputLayersEnum.chunks], changes)
        _set_values(table)


def _replace_chunks_in_block(chunks: _Chunks, change: _Changes) -> None:
    if not chunks:
        return

    if not isinstance(chunks[0], str):
        msg = "The chunks is not a list of strings"
        raise TypeError(msg)

    for i in range(len(chunks)):
        k = chunks[i]
        if k in change and isinstance(k, str):
            chunks[i] = change[k]
        else:
            msg = (
                f"the chunks contains an id: {k} "
                f"that is not present in the to_change dictionary"
            )
            raise KeyError(msg)


def _set_values(table: _TableWithChunks) -> None:
    values: AnyList = []
    # chunks = len(item[InputLayersEnum.chunks])
    for chunk in table[InputLayersEnum.chunks]:
        if InputLayersEnum.values not in chunk:
            msg = f"The chunk does not contain the key {InputLayersEnum.values}"
            raise KeyError(msg)
        if not isinstance(chunk[InputLayersEnum.values], MutableSequence):
            msg = (
                f"The chunk values are not a list, "
                f"but {type(chunk[InputLayersEnum.values])}"
            )
            raise TypeError(msg)

        values.extend(chunk[InputLayersEnum.values])

    table[InputLayersEnum.values] = values
    table[InputLayersEnum.chunks] = []
    # item[InputLayersEnum.chunks] = chunks
