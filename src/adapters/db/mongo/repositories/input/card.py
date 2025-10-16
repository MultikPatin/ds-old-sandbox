from beanie.operators import GTE, LT, In
from common.core.custom_types import AnyList
from common.core.dtos import (
    CursorPageDTO,
    CursorParamsDTO,
    LimitOffsetPageDTO,
    LimitOffsetParamsDTO,
    PagesPageDTO,
    PagesParamsDTO,
)
from common.core.enums import CreateUpdateEnum, LifeStatusEnum
from common.mongo import (
    Base,
    convert_to_id,
    cursor_paginator,
    limit_offset_paginator,
    page_paginator,
)
from pymongo.asynchronous.client_session import AsyncClientSession

from src.application.dtos.db.input import InputCardDB
from src.application.dtos.filters import InputCardFilters


class InputCardRepository(Base):
    async def get_all_like_pages(
        self,
        params: PagesParamsDTO,
        filters: InputCardFilters,
        session: AsyncClientSession | None = None,
    ) -> PagesPageDTO[InputCardDB]:
        conditions = await self._create_conditions(filters)
        sort = filters.live_time_sort.value if filters.live_time_sort else None
        return await page_paginator(
            query=self._collection.find_many(*conditions, session=session),
            session=session,
            params=params,
            sort=sort,
            items_return_type=InputCardDB,
        )

    async def get_all_like_limit_offset(
        self,
        params: LimitOffsetParamsDTO,
        filters: InputCardFilters,
        session: AsyncClientSession | None = None,
    ) -> LimitOffsetPageDTO[InputCardDB]:
        conditions = await self._create_conditions(filters)
        sort = filters.live_time_sort.value if filters.live_time_sort else None
        return await limit_offset_paginator(
            query=self._collection.find_many(*conditions, session=session),
            session=session,
            params=params,
            sort=sort,
            items_return_type=InputCardDB,
        )

    async def get_all_like_cursor(
        self,
        params: CursorParamsDTO,
        filters: InputCardFilters,
        session: AsyncClientSession | None = None,
    ) -> CursorPageDTO[InputCardDB]:
        conditions = await self._create_conditions(filters)
        sort = filters.live_time_sort.value if filters.live_time_sort else None
        return await cursor_paginator(
            query=self._collection.find_many(*conditions, session=session),
            session=session,
            params=params,
            sort=sort,
            items_return_type=InputCardDB,
        )

    async def _create_conditions(self, filters: InputCardFilters) -> AnyList:
        conditions: AnyList = [
            In(
                self._collection.layout.id,
                [convert_to_id(_id) for _id in filters.layout_ids],
            )
        ]

        match filters.life_action_field:
            case CreateUpdateEnum.created:
                if filters.period_start:
                    conditions.append(
                        GTE(self._collection.created, filters.period_start)
                    )
                if filters.period_end:
                    conditions.append(
                        LT(self._collection.created, filters.period_end)
                    )
            case CreateUpdateEnum.updated:
                if filters.period_start:
                    conditions.append(
                        GTE(self._collection.updated, filters.period_start)
                    )
                if filters.period_end:
                    conditions.append(
                        LT(self._collection.updated, filters.period_end)
                    )

        if filters.status:
            conditions.append(self._collection.status == filters.status)
        else:
            conditions.append(self._collection.status != LifeStatusEnum.deleted)
        return conditions
