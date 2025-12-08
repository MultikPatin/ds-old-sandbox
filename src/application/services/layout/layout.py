from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from common.core.dtos.pagination import (
        CursorPageDTO,
        LimitOffsetPageDTO,
        PagesPageDTO,
    )
    from common.core.protocols import SessionProtocol

    from src.application.dtos import LayoutWithBlockLayersDTO
    from src.application.dtos.db import (
        LayoutDB,
        LayoutFullLinks,
        LayoutShortDTO,
    )
    from src.application.protocols import (
        LayoutFiltersProtocol,
        LayoutRepositoryProtocol,
        LayoutShortCursorFiltersProtocol,
        LayoutShortLimitOffsetFiltersProtocol,
        LayoutShortPagesFiltersProtocol,
        LayoutToolsServiceProtocol,
    )


class LayoutService:
    def __init__(
        self,
        repo: "LayoutRepositoryProtocol[SessionProtocol]",
        *,
        tools_service: "LayoutToolsServiceProtocol",
    ):
        self._repo = repo
        self._tools = tools_service

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
    ) -> "LayoutWithBlockLayersDTO":
        instance = await self._repo.get_by_key(key, session=session)
        return await self._tools.replace_layers(
            instance, filters, session=session
        )

    async def get_with_layers(
        self,
        _id: str,
        filters: "LayoutFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "LayoutWithBlockLayersDTO":
        instance = await self._repo.get_full_links(_id, session=session)
        return await self._tools.replace_layers(
            instance, filters, session=session
        )

    async def get_by_input(
        self,
        _id: str,
        filters: "LayoutFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "LayoutWithBlockLayersDTO":
        layout_id = await self._tools.get_id_by_input(_id, session=session)

        return await self.get_with_layers(layout_id, filters, session=session)

    async def get_ids_by(
        self, key: str, *, session: "SessionProtocol"
    ) -> list[str]:
        return await self._repo.get_ids_by(key, session=session)
