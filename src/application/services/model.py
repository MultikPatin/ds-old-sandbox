from common.core.dtos.pagination import (
    CursorPageDTO,
    CursorParamsDTO,
    LimitOffsetPageDTO,
    LimitOffsetParamsDTO,
    PagesPageDTO,
    PagesParamsDTO,
)
from common.core.protocols import SessionProtocol

from src.application.dtos.db.model import ModelDB, ModelWithPublishedLayoutID
from src.application.dtos.filters import ModelFilters
from src.application.protocols.repositories.key import KeyRepositoryProtocol
from src.application.protocols.repositories.model import ModelRepositoryProtocol


class ModelService:
    def __init__(
        self,
        repo: ModelRepositoryProtocol[SessionProtocol],
        key_repo: KeyRepositoryProtocol[SessionProtocol],
    ):
        self._repo = repo
        self._key_repo = key_repo

    async def get_by_layout_id(
        self, _id: str, *, session: SessionProtocol | None = None
    ) -> ModelDB:
        key = await self._key_repo.get_by_layout_id(_id, session=session)
        return await self._repo.get(key.model, session=session)

    async def get_all_like_pages(
        self,
        params: PagesParamsDTO,
        filters: ModelFilters,
        *,
        session: SessionProtocol | None = None,
    ) -> PagesPageDTO[ModelWithPublishedLayoutID]:
        return await self._repo.get_all_like_pages(
            params, filters, session=session
        )

    async def get_all_like_limit_offset(
        self,
        params: LimitOffsetParamsDTO,
        filters: ModelFilters,
        *,
        session: SessionProtocol | None = None,
    ) -> LimitOffsetPageDTO[ModelWithPublishedLayoutID]:
        return await self._repo.get_all_like_limit_offset(
            params, filters, session=session
        )

    async def get_all_like_cursor(
        self,
        params: CursorParamsDTO,
        filters: ModelFilters,
        *,
        session: SessionProtocol | None = None,
    ) -> CursorPageDTO[ModelWithPublishedLayoutID]:
        return await self._repo.get_all_like_cursor(
            params, filters, session=session
        )
