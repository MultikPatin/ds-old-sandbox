from typing import TYPE_CHECKING

from abgroup_core.utils import generate_random_string

from src.application.dtos.db.layout import (
    LayoutMessageCreateDTO,
)

if TYPE_CHECKING:
    from abgroup_core.dtos.pagination import (
        CursorPageDTO,
        LimitOffsetPageDTO,
        PagesPageDTO,
    )
    from abgroup_core.protocols import SessionProtocol

    from src.application.dtos import LayoutMessageCreate
    from src.application.dtos.db.layout import (
        LayoutMessageDB,
        LayoutMessageUpdateDTO,
    )
    from src.application.protocols import (
        LayoutMessageCursorFiltersProtocol,
        LayoutMessageLimitOffsetFiltersProtocol,
        LayoutMessagePagesFiltersProtocol,
        LayoutMessageRepositoryProtocol,
    )


class LayoutMessageService:
    def __init__(
        self,
        repo: "LayoutMessageRepositoryProtocol[SessionProtocol]",
    ) -> None:
        self._repo = repo

    async def get(
        self, _id: str, *, session: "SessionProtocol"
    ) -> "LayoutMessageDB":
        return await self._repo.get(_id, session=session)

    async def add(
        self,
        condition: "LayoutMessageCreate",
        *,
        session: "SessionProtocol",
    ) -> "LayoutMessageDB":
        return await self._repo.add(
            LayoutMessageCreateDTO(
                **condition.model_dump(),
                key=generate_random_string(),
            ),
            session=session,
        )

    async def update(
        self,
        _id: str,
        condition: "LayoutMessageUpdateDTO",
        *,
        session: "SessionProtocol",
    ) -> "LayoutMessageDB":
        return await self._repo.update(_id, condition, session=session)

    async def get_all_pages(
        self,
        filters: "LayoutMessagePagesFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "PagesPageDTO[LayoutMessageDB]":
        return await self._repo.get_all_pages(filters, session=session)

    async def get_all_limit_offset(
        self,
        filters: "LayoutMessageLimitOffsetFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "LimitOffsetPageDTO[LayoutMessageDB]":
        return await self._repo.get_all_limit_offset(filters, session=session)

    async def get_all_cursor(
        self,
        filters: "LayoutMessageCursorFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "CursorPageDTO[LayoutMessageDB]":
        return await self._repo.get_all_cursor(filters, session=session)
