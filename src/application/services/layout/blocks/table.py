from typing import TYPE_CHECKING

from src.application.dtos import LayoutTableWithLayersDTO

if TYPE_CHECKING:
    from abgroup_core.dtos.pagination import (
        CursorPageDTO,
        LimitOffsetPageDTO,
        PagesPageDTO,
    )
    from abgroup_core.protocols import SessionProtocol

    from src.application.dtos.db.layout import LayoutTableDB
    from src.application.protocols import (
        LayersFetcherFiltersProtocol,
        LayoutBlocksFetcherProtocol,
        LayoutTableCursorFiltersProtocol,
        LayoutTableLimitOffsetFiltersProtocol,
        LayoutTablePagesFiltersProtocol,
        LayoutTableRepositoryProtocol,
    )


class LayoutTableService:
    def __init__(
        self,
        repo: "LayoutTableRepositoryProtocol[SessionProtocol]",
        *,
        fetcher_service: "LayoutBlocksFetcherProtocol",
    ) -> None:
        self._repo = repo
        self._fetcher = fetcher_service

    async def get_all_pages(
        self,
        filters: "LayoutTablePagesFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "PagesPageDTO[LayoutTableDB]":
        return await self._repo.get_all_pages(filters, session=session)

    async def get_all_limit_offset(
        self,
        filters: "LayoutTableLimitOffsetFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "LimitOffsetPageDTO[LayoutTableDB]":
        return await self._repo.get_all_limit_offset(filters, session=session)

    async def get_all_cursor(
        self,
        filters: "LayoutTableCursorFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "CursorPageDTO[LayoutTableDB]":
        return await self._repo.get_all_cursor(filters, session=session)

    async def get_with_layers(
        self,
        _id: str,
        filters: "LayersFetcherFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> LayoutTableWithLayersDTO:
        instance = await self._repo.get(_id, session=session)
        obj = instance.model_dump()

        await self._fetcher.fetch_block(
            obj,  # type: ignore
            session=session,
            layers=filters.layers,
            in_place=True,
        )

        return LayoutTableWithLayersDTO.model_validate(obj)
