import asyncio
from collections.abc import Coroutine
from typing import TYPE_CHECKING, Any

from src.application.dtos import LayoutWithBlockLayersDTO
from src.application.enums import LayoutLayersEnum

from .replacer import get_ids_by_layers, replace_layers

if TYPE_CHECKING:
    from common.core.protocols import SessionProtocol

    from src.application.dtos.db import LayoutWithBlocks
    from src.application.protocols import (
        InputRepositoryProtocol,
        LayoutDefaultRepositoryProtocol,
        LayoutFiltersProtocol,
        LayoutSchemaRepositoryProtocol,
        LayoutStyleRepositoryProtocol,
        LayoutValidationRepositoryProtocol,
    )


class LayoutToolsService:
    def __init__(
        self,
        *,
        input_repo: "InputRepositoryProtocol[SessionProtocol]",
        schema_repo: "LayoutSchemaRepositoryProtocol[SessionProtocol]",
        style_repo: "LayoutStyleRepositoryProtocol[SessionProtocol]",
        validation_repo: "LayoutValidationRepositoryProtocol[SessionProtocol]",
        default_repo: "LayoutDefaultRepositoryProtocol[SessionProtocol]",
    ):
        self._input = input_repo
        self._schema = schema_repo
        self._style = style_repo
        self._validation = validation_repo
        self._default = default_repo

    async def replace_layers(
        self,
        instance: "LayoutWithBlocks",
        filters: "LayoutFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> LayoutWithBlockLayersDTO:
        ids = get_ids_by_layers(instance, exclude=filters.excluded_layers)
        if not ids:
            return LayoutWithBlockLayersDTO.model_validate(
                instance.model_dump()
            )

        keys: list[LayoutLayersEnum] = []
        coro: list[Coroutine[None, None, list[Any]]] = []
        for k, v in ids.items():
            if not v:
                continue

            keys.append(k)

            if k == LayoutLayersEnum.schemas:
                coro.append(self._schema.get_by_ids(v, session=session))
            elif k == LayoutLayersEnum.styles:
                coro.append(self._style.get_by_ids(v, session=session))
            elif k == LayoutLayersEnum.validations:
                coro.append(self._validation.get_by_ids(v, session=session))
            elif k == LayoutLayersEnum.defaults:
                coro.append(self._default.get_by_ids(v, session=session))

        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(c) for c in coro]

        results = [t.result() for t in tasks]

        changes = {}
        for k, r in zip(keys, results, strict=False):
            changes[k] = {m.id: m.model_dump() for m in r}

        return LayoutWithBlockLayersDTO.model_validate(
            replace_layers(instance, changes)
        )

    async def get_id_by_input(
        self, _id: str, *, session: "SessionProtocol"
    ) -> str:
        return await self._input.get_layout_id(_id, session=session)
