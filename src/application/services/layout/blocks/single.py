from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from abgroup_core.dtos.pagination import (
        CursorPageDTO,
        LimitOffsetPageDTO,
        PagesPageDTO,
    )
    from abgroup_core.protocols import SessionProtocol

    from src.application.dtos.db.layout import (
        LayoutSingleDB,
    )
    from src.application.protocols import (
        LayoutSingleCursorFiltersProtocol,
        LayoutSingleLimitOffsetFiltersProtocol,
        LayoutSinglePagesFiltersProtocol,
        LayoutSingleRepositoryProtocol,
    )


class LayoutSingleService:
    def __init__(
        self,
        repo: "LayoutSingleRepositoryProtocol[SessionProtocol]",
    ) -> None:
        self._repo = repo

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
