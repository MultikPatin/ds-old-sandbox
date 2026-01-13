from typing import TYPE_CHECKING

from abgroup_core.custom_types import AnyList
from abgroup_core.enums import CreateUpdateEnum, LifeStatusEnum
from common.mongo import (
    Base,
    KeysEnum,
    convert_to_id,
    paginator_cursor,
    paginator_limit_offset,
    paginator_pages,
    prepare_sort,
)

from src.adapters.db.mongo.projections import InputCardProjection
from src.application.dtos.db import InputCardDTO

if TYPE_CHECKING:
    from abgroup_core.dtos.pagination import (
        CursorPageDTO,
        LimitOffsetPageDTO,
        PagesPageDTO,
    )
    from beanie import Document
    from beanie.odm.queries.find import FindMany
    from pydantic import BaseModel
    from pymongo.asynchronous.client_session import AsyncClientSession

    from src.application.protocols import (
        InputCardCursorFiltersProtocol,
        InputCardFiltersProtocol,
        InputCardLimitOffsetFiltersProtocol,
        InputCardPagesFiltersProtocol,
    )

type FindManyQueryType[DocType, ProjectionModelType] = (
    FindMany[DocType] | FindMany[ProjectionModelType]
)


class InputCardRepository(Base):
    async def get_all_pages(
        self,
        filters: "InputCardPagesFiltersProtocol",
        *,
        session: "AsyncClientSession",
    ) -> "PagesPageDTO[InputCardDTO]":
        return await paginator_pages(
            query=self._create_query(filters, session=session),
            params=filters,
            session=session,
            sort=prepare_sort(filters.life_time_sort, self._collection),
            items_return_type=InputCardDTO,
            projection_model=InputCardProjection,
        )

    async def get_all_limit_offset(
        self,
        filters: "InputCardLimitOffsetFiltersProtocol",
        *,
        session: "AsyncClientSession",
    ) -> "LimitOffsetPageDTO[InputCardDTO]":
        return await paginator_limit_offset(
            query=self._create_query(filters, session=session),
            params=filters,
            session=session,
            sort=prepare_sort(filters.life_time_sort, self._collection),
            items_return_type=InputCardDTO,
            projection_model=InputCardProjection,
        )

    async def get_all_cursor(
        self,
        filters: "InputCardCursorFiltersProtocol",
        *,
        session: "AsyncClientSession",
    ) -> "CursorPageDTO[InputCardDTO]":
        return await paginator_cursor(
            query=self._create_query(filters, session=session),
            params=filters,
            session=session,
            sort=prepare_sort(filters.life_time_sort, self._collection),
            items_return_type=InputCardDTO,
            projection_model=InputCardProjection,
        )

    def _create_query[DocType: Document, ProjectionModelType: BaseModel](
        self,
        filters: "InputCardFiltersProtocol",
        *,
        session: "AsyncClientSession",
    ) -> FindManyQueryType[DocType, ProjectionModelType]:
        conditions = self._create_conditions(filters)
        return self._collection.find_many(*conditions, session=session)

    def _create_conditions(
        self, filters: "InputCardFiltersProtocol"
    ) -> AnyList:
        conditions: AnyList = [
            {
                self._collection.layout.id: {
                    KeysEnum.in_: [
                        convert_to_id(_id) for _id in filters.layout_ids
                    ]
                }
            }
        ]

        if filters.life_action_field == CreateUpdateEnum.created:
            if filters.period_start:
                conditions.append(
                    {
                        self._collection.created: {
                            KeysEnum.gte: filters.period_start
                        }
                    }
                )
            if filters.period_end:
                conditions.append(
                    {
                        self._collection.created: {
                            KeysEnum.lt: filters.period_end
                        }
                    }
                )
        elif filters.life_action_field == CreateUpdateEnum.updated:
            if filters.period_start:
                conditions.append(
                    {
                        self._collection.updated: {
                            KeysEnum.gte: filters.period_start
                        }
                    }
                )
            if filters.period_end:
                conditions.append(
                    {
                        self._collection.updated: {
                            KeysEnum.lt: filters.period_end
                        }
                    }
                )

        if filters.status:
            conditions.append(self._collection.status == filters.status)
        else:
            conditions.append(self._collection.status != LifeStatusEnum.deleted)

        return conditions
