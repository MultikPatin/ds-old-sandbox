from common.core.custom_types import AnyList
from common.core.dtos import (
    CursorPageDTO,
    CursorParamsDTO,
    LimitOffsetPageDTO,
    LimitOffsetParamsDTO,
    PagesPageDTO,
    PagesParamsDTO,
)
from common.core.enums import LifeStatusEnum
from common.mongo import (
    GetMixin,
    cursor_paginator,
    limit_offset_paginator,
    page_paginator,
)
from pymongo.asynchronous.client_session import AsyncClientSession

from src.application.dtos.db.model import ModelDB, ModelWithPublishedLayoutID
from src.application.dtos.filters import ModelFilters


class ModelRepository(GetMixin[ModelDB]):
    async def get_all_like_pages(
        self,
        params: PagesParamsDTO,
        filters: ModelFilters,
        *,
        session: AsyncClientSession | None = None,
    ) -> PagesPageDTO[ModelWithPublishedLayoutID]:
        conditions = await self._create_conditions(filters)
        return await page_paginator(
            query=self._collection.find_many(*conditions, session=session),
            params=params,
            sort=filters.sort,
            items_return_type=ModelWithPublishedLayoutID,
            fetch_links=True,
            nesting_depths_per_field={"keys": 2},
        )

    async def get_all_like_limit_offset(
        self,
        params: LimitOffsetParamsDTO,
        filters: ModelFilters,
        *,
        session: AsyncClientSession | None = None,
    ) -> LimitOffsetPageDTO[ModelWithPublishedLayoutID]:
        conditions = await self._create_conditions(filters)
        return await limit_offset_paginator(
            query=self._collection.find_many(*conditions, session=session),
            params=params,
            sort=filters.sort,
            session=session,
            items_return_type=ModelWithPublishedLayoutID,
            fetch_links=True,
            nesting_depths_per_field={"keys": 2},
        )

    async def get_all_like_cursor(
        self,
        params: CursorParamsDTO,
        filters: ModelFilters,
        *,
        session: AsyncClientSession | None = None,
    ) -> CursorPageDTO[ModelWithPublishedLayoutID]:
        conditions = await self._create_conditions(filters)
        return await cursor_paginator(
            query=self._collection.find_many(*conditions, session=session),
            params=params,
            sort=filters.sort,
            session=session,
            items_return_type=ModelWithPublishedLayoutID,
            fetch_links=True,
            nesting_depths_per_field={"keys": 2},
        )

    async def _create_conditions(self, filters: ModelFilters) -> AnyList:
        conditions: AnyList = []
        if filters.status:
            conditions.append(self._collection.status == filters.status)
        else:
            conditions.append(
                self._collection.status == LifeStatusEnum.published
            )
        return conditions
