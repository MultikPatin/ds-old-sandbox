from typing import TYPE_CHECKING

from src.application.dtos import LayoutSingleWithLayersDTO

if TYPE_CHECKING:
    from abgroup_core.dtos.pagination import (
        CursorPageDTO,
        LimitOffsetPageDTO,
        PagesPageDTO,
    )
    from abgroup_core.protocols import SessionProtocol

    from src.application.dtos.db.layout import LayoutSingleDB
    from src.application.protocols import (
        LayersFetcherFiltersProtocol,
        LayoutBlocksFetcherProtocol,
        LayoutSingleCursorFiltersProtocol,
        LayoutSingleLimitOffsetFiltersProtocol,
        LayoutSinglePagesFiltersProtocol,
        LayoutSingleRepositoryProtocol,
    )


class LayoutSingleService:
    def __init__(
        self,
        repo: "LayoutSingleRepositoryProtocol[SessionProtocol]",
        *,
        fetcher_service: "LayoutBlocksFetcherProtocol",
    ) -> None:
        self._repo = repo
        self._fetcher = fetcher_service

    async def get_all_pages(
        self,
        filters: "LayoutSinglePagesFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "PagesPageDTO[LayoutSingleDB]":
        return await self._repo.get_all_pages(filters, session=session)

    async def get_all_limit_offset(
        self,
        filters: "LayoutSingleLimitOffsetFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "LimitOffsetPageDTO[LayoutSingleDB]":
        return await self._repo.get_all_limit_offset(filters, session=session)

    async def get_all_cursor(
        self,
        filters: "LayoutSingleCursorFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "CursorPageDTO[LayoutSingleDB]":
        return await self._repo.get_all_cursor(filters, session=session)

    async def get_with_layers(
        self,
        _id: str,
        filters: "LayersFetcherFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> LayoutSingleWithLayersDTO:
        instance = await self._repo.get(_id, session=session)
        obj = instance.model_dump()

        await self._fetcher.fetch_block(
            obj,  # type: ignore
            session=session,
            layers=filters.layers,
            in_place=True,
        )

        return LayoutSingleWithLayersDTO.model_validate(obj)
