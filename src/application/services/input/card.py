from typing import TYPE_CHECKING

from common.core.custom_types import AnyDict

if TYPE_CHECKING:
    from common.core.dtos.pagination import (
        CursorPageDTO,
        LimitOffsetPageDTO,
        PagesPageDTO,
    )
    from common.core.protocols import SessionProtocol

    from src.application.dtos.db import InputCardDTO
    from src.application.protocols import (
        InputCardCursorFiltersProtocol,
        InputCardInRichFiltersProtocol,
        InputCardLimitOffsetFiltersProtocol,
        InputCardPagesFiltersProtocol,
        InputCardRepositoryProtocol,
        LayoutServiceProtocol,
    )


class InputCardSrvice:
    def __init__(
        self,
        repo: "InputCardRepositoryProtocol[SessionProtocol]",
        *,
        layout_service: "LayoutServiceProtocol",
    ):
        self._repo = repo
        self._layout = layout_service

    async def get_all_pages(
        self,
        filters: "InputCardPagesFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "PagesPageDTO[InputCardDTO]":
        await self._enrich(filters, session=session)
        return await self._repo.get_all_pages(filters, session=session)

    async def get_all_limit_offset(
        self,
        filters: "InputCardLimitOffsetFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "LimitOffsetPageDTO[InputCardDTO]":
        await self._enrich(filters, session=session)
        return await self._repo.get_all_limit_offset(filters, session=session)

    async def get_all_cursor(
        self,
        filters: "InputCardCursorFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "CursorPageDTO[InputCardDTO]":
        await self._enrich(filters, session=session)
        return await self._repo.get_all_cursor(filters, session=session)

    async def _enrich(
        self,
        filters: "InputCardInRichFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> None:
        filters.layout_ids = await self._layout.get_ids_by(
            filters.layouts_key, session=session
        )


async def generate_card(layout_id: str) -> list[AnyDict] | None:
    # TODO: Реализовать генерацию карточки
    # input_card = await self._layout_card_repo.get_by_layout_id(layout_id)
    # if input_card is None:
    #     return None
    return [{"title": "incorrect path", "value": "incorrect path"}]
