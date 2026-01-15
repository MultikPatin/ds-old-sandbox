from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from abgroup_core.dtos.pagination import (
        CursorPageDTO,
        LimitOffsetPageDTO,
        PagesPageDTO,
    )
    from abgroup_core.protocols import SessionProtocol

    from src.application.dtos.db.layout import LayoutTableDB
    from src.application.protocols import (
        LayoutTableCursorFiltersProtocol,
        LayoutTableLimitOffsetFiltersProtocol,
        LayoutTablePagesFiltersProtocol,
        LayoutTableRepositoryProtocol,
    )


class LayoutTableService:
    def __init__(
        self,
        repo: "LayoutTableRepositoryProtocol[SessionProtocol]",
    ) -> None:
        self._repo = repo

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
