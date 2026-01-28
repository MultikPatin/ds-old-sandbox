import asyncio
from collections.abc import Coroutine, Iterable, MutableMapping, MutableSequence
from copy import deepcopy
from typing import TYPE_CHECKING, Any

from src.application.enums import LayoutLayersEnum

from .extraction import (
    _collect_blocks,
    _collect_layer_ids,
    _extract_layers_ids,
)
from .helpers import (
    _Block,
    _BlocksNames,
    _FetchedLayersMap,
    _IDsByLayers,
    _LayersNames,
    _Layout,
)
from .replacement import (
    _replace_block,
    _replace_blocks,
    _replace_layout,
)

if TYPE_CHECKING:
    from abgroup_core.protocols import GetterByIDsProtocol, SessionProtocol

    from src.application.protocols import (
        LayoutDefaultRepositoryProtocol,
        LayoutSchemaRepositoryProtocol,
        LayoutStyleRepositoryProtocol,
        LayoutValidationRepositoryProtocol,
    )


class LayoutBlocksFetcher:
    def __init__(
        self,
        *,
        schema_repo: "LayoutSchemaRepositoryProtocol[SessionProtocol]",
        style_repo: "LayoutStyleRepositoryProtocol[SessionProtocol]",
        validation_repo: "LayoutValidationRepositoryProtocol[SessionProtocol]",
        default_repo: "LayoutDefaultRepositoryProtocol[SessionProtocol]",
    ) -> None:
        self._schema = schema_repo
        self._style = style_repo
        self._validation = validation_repo
        self._default = default_repo

    async def fetch_block(
        self,
        obj: _Block,
        *,
        session: "SessionProtocol",
        layers: _LayersNames,
        in_place: bool = False,
    ) -> _Block:
        if not in_place:
            obj = deepcopy(obj)

        ids = _extract_layers_ids(obj, layers)

        if not ids:
            layers_map: _FetchedLayersMap = {}
        else:
            layers_map = await self._fetch_layers(ids, session=session)

        _replace_block(obj, layers_map)

        return obj

    async def fetch_blocks(
        self,
        objs: Iterable[_Block],
        *,
        session: "SessionProtocol",
        layers: _LayersNames,
        in_place: bool = False,
    ) -> Iterable[_Block]:
        if not in_place:
            objs = deepcopy(objs)

        ids = _collect_layer_ids(objs, layers)

        if not ids:
            layers_map: _FetchedLayersMap = {}
        else:
            layers_map = await self._fetch_layers(ids, session=session)

        _replace_blocks(objs, layers_map)

        return objs

    async def fetch_layout(
        self,
        obj: _Layout,
        *,
        session: "SessionProtocol",
        blocks: _BlocksNames,
        layers: _LayersNames,
        in_place: bool = False,
    ) -> _Layout:
        if not in_place:
            obj = deepcopy(obj)

        ids = _collect_layer_ids(_collect_blocks(obj, blocks), layers)

        if not ids:
            layers_map: _FetchedLayersMap = {}
        else:
            layers_map = await self._fetch_layers(ids, session=session)

        _replace_layout(obj, blocks, layers_map)

        return obj

    async def _fetch_layers(
        self, ids: _IDsByLayers, *, session: "SessionProtocol"
    ) -> _FetchedLayersMap:
        keys: MutableSequence[LayoutLayersEnum] = []
        coro: MutableSequence[Coroutine[None, None, list[Any]]] = []
        repos: MutableMapping[
            LayoutLayersEnum, GetterByIDsProtocol[Any, SessionProtocol]
        ] = {
            LayoutLayersEnum.schemas: self._schema,
            LayoutLayersEnum.styles: self._style,
            LayoutLayersEnum.validations: self._validation,
            LayoutLayersEnum.defaults: self._default,
        }

        for k, v in ids.items():
            if not v:
                continue

            keys.append(k)
            coro.append(repos[k].get_by_ids(v, session=session))

        async with asyncio.TaskGroup() as tg:
            ts = [tg.create_task(c) for c in coro]

        return {
            k: {m.id: m.model_dump() for m in r}
            for k, r in zip(keys, [t.result() for t in ts], strict=False)
        }
