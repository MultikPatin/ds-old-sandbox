from collections.abc import Iterable, MutableMapping, MutableSequence, Set
from typing import Protocol

from abgroup_core.protocols import SessionProtocol

from src.application.enums import LayoutBlocksEnum, LayoutLayersEnum

type _Layer = MutableSequence[str] | MutableSequence[MutableSequence[str]]
type _Block = MutableMapping[LayoutLayersEnum, _Layer | None]
type _Layout = MutableMapping[LayoutBlocksEnum, Iterable[_Block] | None]


class LayoutBlocksFetcherProtocol(Protocol):
    async def fetch_block(
        self,
        obj: _Block,
        *,
        session: "SessionProtocol",
        layers: Set[LayoutLayersEnum],
        in_place: bool = False,
    ) -> _Block: ...
    async def fetch_blocks(
        self,
        objs: Iterable[_Block],
        *,
        session: "SessionProtocol",
        layers: Set[LayoutLayersEnum],
        in_place: bool = False,
    ) -> Iterable[_Block]: ...
    async def fetch_layout(
        self,
        obj: _Layout,
        *,
        session: "SessionProtocol",
        blocks: Set[LayoutBlocksEnum],
        layers: Set[LayoutLayersEnum],
        in_place: bool = False,
    ) -> _Layout: ...
