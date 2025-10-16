from common.core.custom_types import AnyDict
from common.core.dtos.pagination import (
    CursorPageDTO,
    CursorParamsDTO,
    LimitOffsetPageDTO,
    LimitOffsetParamsDTO,
    PagesPageDTO,
    PagesParamsDTO,
)
from common.core.protocols import SessionProtocol

from src.application.dtos.db.input import InputCardDB
from src.application.dtos.filters import InputCardFilters
from src.application.protocols.repositories.input import (
    InputCardRepositoryProtocol,
)
from src.application.protocols.repositories.key import KeyRepositoryProtocol


class InputCardSrvice:
    def __init__(
        self,
        repo: InputCardRepositoryProtocol[SessionProtocol],
        key_repo: KeyRepositoryProtocol[SessionProtocol],
    ):
        self._repo = repo
        self._key_repo = key_repo

    async def get_all_like_pages(
        self,
        params: PagesParamsDTO,
        filters: InputCardFilters,
        *,
        session: SessionProtocol | None = None,
    ) -> PagesPageDTO[InputCardDB]:
        filters.layout_ids = await self._get_layout_ids(
            filters.model_id, session=session
        )
        return await self._repo.get_all_like_pages(
            params, filters, session=session
        )

    async def get_all_like_limit_offset(
        self,
        params: LimitOffsetParamsDTO,
        filters: InputCardFilters,
        *,
        session: SessionProtocol | None = None,
    ) -> LimitOffsetPageDTO[InputCardDB]:
        layout_ids = await self._get_layout_ids(
            filters.model_id, session=session
        )
        filters.layout_ids = layout_ids
        return await self._repo.get_all_like_limit_offset(
            params, filters, session=session
        )

    async def get_all_like_cursor(
        self,
        params: CursorParamsDTO,
        filters: InputCardFilters,
        *,
        session: SessionProtocol | None = None,
    ) -> CursorPageDTO[InputCardDB]:
        layout_ids = await self._get_layout_ids(
            filters.model_id, session=session
        )
        filters.layout_ids = layout_ids
        return await self._repo.get_all_like_cursor(
            params, filters, session=session
        )

    async def _get_layout_ids(
        self,
        model_id: str,
        *,
        session: SessionProtocol | None = None,
    ) -> list[str]:
        # TODO: Вероятно кеширования ответа get_by_model_id
        # TODO: Продумать механизм инвалидации кеша
        keys = await self._key_repo.get_by_model_id(model_id, session=session)
        return [key.layout for key in keys]


async def generate_card(layout_id: str) -> list[AnyDict] | None:
    # TODO: Реализовать генерацию карточки
    # input_card = await self._layout_card_repo.get_by_layout_id(layout_id)
    # if input_card is None:
    #     return None
    return [{"title": "incorrect path", "value": "incorrect path"}]
