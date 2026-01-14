from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from abgroup_core.dtos.pagination import (
        CursorPageDTO,
        LimitOffsetPageDTO,
        PagesPageDTO,
    )
    from abgroup_core.protocols import SessionProtocol

    from src.application.dtos.db.layout import (
        LayoutMessageDB,
    )
    from src.application.protocols import (
        LayoutMassageCursorFiltersProtocol,
        LayoutMassageLimitOffsetFiltersProtocol,
        LayoutMassagePagesFiltersProtocol,
        LayoutMessageRepositoryProtocol,
    )


class LayoutMessageService:
    def __init__(
        self,
        repo: "LayoutMessageRepositoryProtocol[SessionProtocol]",
    ) -> None:
        self._repo = repo

    async def get_all_pages(
        self,
        filters: "LayoutMassagePagesFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "PagesPageDTO[LayoutMessageDB]":
        return await self._repo.get_all_pages(filters, session=session)

    async def get_all_limit_offset(
        self,
        filters: "LayoutMassageLimitOffsetFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "LimitOffsetPageDTO[LayoutMessageDB]":
        return await self._repo.get_all_limit_offset(filters, session=session)

    async def get_all_cursor(
        self,
        filters: "LayoutMassageCursorFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "CursorPageDTO[LayoutMessageDB]":
        return await self._repo.get_all_cursor(filters, session=session)
