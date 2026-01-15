from typing import TYPE_CHECKING

from abgroup_core.custom_types import AnyList
from common.mongo import (
    AddMixin,
    GetMixin,
    paginator_cursor,
    paginator_limit_offset,
    paginator_pages,
    # prepare_sort,
)

from src.application.dtos.db.layout import (
    LayoutMessageCreateDTO,
    LayoutMessageDB,
)

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
        LayoutMessageCursorFiltersProtocol,
        LayoutMessageLimitOffsetFiltersProtocol,
        LayoutMessagePagesFiltersProtocol,
        LayoutMessagePaginationFiltersProtocol,
    )


type FindManyQueryType[DocType, ProjectionModelType] = (
    FindMany[DocType] | FindMany[ProjectionModelType]
)


class LayoutMessageRepository(
    GetMixin[LayoutMessageDB],
    AddMixin[LayoutMessageCreateDTO, LayoutMessageDB],
):
    async def get_all_pages(
        self,
        filters: "LayoutMessagePagesFiltersProtocol",
        *,
        session: "AsyncClientSession",
    ) -> "PagesPageDTO[LayoutMessageDB]":
        return await paginator_pages(
            query=self._pagination_query(filters, session=session),
            params=filters,
            session=session,
            # sort=prepare_sort(filters.life_time_sort, self._collection),
            items_return_type=LayoutMessageDB,
        )

    async def get_all_limit_offset(
        self,
        filters: "LayoutMessageLimitOffsetFiltersProtocol",
        *,
        session: "AsyncClientSession",
    ) -> "LimitOffsetPageDTO[LayoutMessageDB]":
        return await paginator_limit_offset(
            query=self._pagination_query(filters, session=session),
            params=filters,
            session=session,
            # sort=prepare_sort(filters.life_time_sort, self._collection),
            items_return_type=LayoutMessageDB,
        )

    async def get_all_cursor(
        self,
        filters: "LayoutMessageCursorFiltersProtocol",
        *,
        session: "AsyncClientSession",
    ) -> "CursorPageDTO[LayoutMessageDB]":
        return await paginator_cursor(
            query=self._pagination_query(filters, session=session),
            params=filters,
            session=session,
            # sort=prepare_sort(filters.life_time_sort, self._collection),
            items_return_type=LayoutMessageDB,
        )

    def _pagination_query[DocType: Document, ProjectionModelType: BaseModel](
        self,
        filters: "LayoutMessagePaginationFiltersProtocol",
        *,
        session: "AsyncClientSession",
    ) -> FindManyQueryType[DocType, ProjectionModelType]:
        conditions: AnyList = []

        return self._collection.find_many(*conditions, session=session)
