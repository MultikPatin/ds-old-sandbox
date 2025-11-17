import asyncio
from collections.abc import Coroutine
from typing import TYPE_CHECKING, Any

from src.application.dtos import LayoutWithBlockLayersDTO
from src.application.enums import LayoutLayersEnum

from .replacer import get_ids_by_layers, replace_layers

if TYPE_CHECKING:
    from common.core.dtos.pagination import (
        CursorPageDTO,
        LimitOffsetPageDTO,
        PagesPageDTO,
    )
    from common.core.protocols import SessionProtocol

    from src.application.dtos.db import (
        LayoutDB,
        LayoutFullLinks,
        LayoutShortDTO,
        LayoutWithBlocks,
    )
    from src.application.protocols import (
        InputRepositoryProtocol,
        LayoutFiltersProtocol,
        LayoutRepositoryProtocol,
        LayoutSchemaServiceProtocol,
        LayoutShortCursorFiltersProtocol,
        LayoutShortLimitOffsetFiltersProtocol,
        LayoutShortPagesFiltersProtocol,
        LayoutStyleServiceProtocol,
        LayoutValidationServiceProtocol,
    )


class LayoutService:
    def __init__(
        self,
        repo: "LayoutRepositoryProtocol[SessionProtocol]",
        *,
        input_repo: "InputRepositoryProtocol[SessionProtocol]",
        cell_schema_service: "LayoutSchemaServiceProtocol",
        cell_style_service: "LayoutStyleServiceProtocol",
        cell_validation_service: "LayoutValidationServiceProtocol",
    ):
        self._repo = repo
        self._input = input_repo
        self._schema = cell_schema_service
        self._style = cell_style_service
        self._validation = cell_validation_service

    async def get_all_pages(
        self,
        filters: "LayoutShortPagesFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "PagesPageDTO[LayoutShortDTO]":
        return await self._repo.get_all_pages(filters, session=session)

    async def get_all_limit_offset(
        self,
        filters: "LayoutShortLimitOffsetFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "LimitOffsetPageDTO[LayoutShortDTO]":
        return await self._repo.get_all_limit_offset(filters, session=session)

    async def get_all_cursor(
        self,
        filters: "LayoutShortCursorFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "CursorPageDTO[LayoutShortDTO]":
        return await self._repo.get_all_cursor(filters, session=session)

    async def delete_soft(self, _id: str, *, session: "SessionProtocol") -> str:
        return await self._repo.delete_soft(_id, session=session)

    async def get(self, _id: str, *, session: "SessionProtocol") -> "LayoutDB":
        return await self._repo.get(_id, session=session)

    async def get_full_links(
        self, _id: str, *, session: "SessionProtocol"
    ) -> "LayoutFullLinks":
        return await self._repo.get_full_links(_id, session=session)

    async def get_with_layers_by_key(
        self,
        key: str,
        filters: "LayoutFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> LayoutWithBlockLayersDTO:
        layout = await self._repo.get_by_key(key, session=session)
        return await self._get_with_layers(layout, filters, session=session)

    async def get_with_layers(
        self,
        _id: str,
        filters: "LayoutFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> LayoutWithBlockLayersDTO:
        layout = await self._repo.get_full_links(_id, session=session)
        return await self._get_with_layers(layout, filters, session=session)

    async def _get_with_layers(
        self,
        layout: "LayoutWithBlocks",
        filters: "LayoutFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> LayoutWithBlockLayersDTO:
        ids = get_ids_by_layers(layout, exclude=filters.excluded_layers)

        keys: list[LayoutLayersEnum] = []
        coro: list[Coroutine[None, None, list[Any]]] = []
        for k, v in ids.items():
            keys.append(k)

            if k == LayoutLayersEnum.schemas:
                coro.append(self._schema.get_by_ids(v, session=session))
            elif k == LayoutLayersEnum.styles:
                coro.append(self._style.get_by_ids(v, session=session))
            elif k == LayoutLayersEnum.validations:
                coro.append(self._validation.get_by_ids(v, session=session))

        results = await asyncio.gather(*coro)

        changes = {}
        for k, r in zip(keys, results, strict=False):
            changes[k] = {m.id: m.model_dump() for m in r}

        return LayoutWithBlockLayersDTO(**replace_layers(layout, changes))

    async def get_by_input(
        self,
        _id: str,
        filters: "LayoutFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> LayoutWithBlockLayersDTO:
        _id = await self._input.get_layout_id(_id, session=session)
        return await self.get_with_layers(_id, filters, session=session)

    async def get_ids_by(
        self, key: str, *, session: "SessionProtocol"
    ) -> list[str]:
        return await self._repo.get_ids_by(key, session=session)
