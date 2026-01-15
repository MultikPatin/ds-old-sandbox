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

from src.application.dtos.db.layout import LayoutSingleCreateDTO, LayoutSingleDB

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
        LayoutSingleCursorFiltersProtocol,
        LayoutSingleLimitOffsetFiltersProtocol,
        LayoutSinglePagesFiltersProtocol,
        LayoutSinglePaginationFiltersProtocol,
    )


type FindManyQueryType[DocType, ProjectionModelType] = (
    FindMany[DocType] | FindMany[ProjectionModelType]
)


class LayoutSingleRepository(
    GetMixin[LayoutSingleDB],
    AddMixin[LayoutSingleCreateDTO, LayoutSingleDB],
):
    async def get_all_pages(
        self,
        filters: "LayoutSinglePagesFiltersProtocol",
        *,
        session: "AsyncClientSession",
    ) -> "PagesPageDTO[LayoutSingleDB]":
        return await paginator_pages(
            query=self._pagination_query(filters, session=session),
            params=filters,
            session=session,
            # sort=prepare_sort(filters.life_time_sort, self._collection),
            items_return_type=LayoutSingleDB,
        )

    async def get_all_limit_offset(
        self,
        filters: "LayoutSingleLimitOffsetFiltersProtocol",
        *,
        session: "AsyncClientSession",
    ) -> "LimitOffsetPageDTO[LayoutSingleDB]":
        return await paginator_limit_offset(
            query=self._pagination_query(filters, session=session),
            params=filters,
            session=session,
            # sort=prepare_sort(filters.life_time_sort, self._collection),
            items_return_type=LayoutSingleDB,
        )

    async def get_all_cursor(
        self,
        filters: "LayoutSingleCursorFiltersProtocol",
        *,
        session: "AsyncClientSession",
    ) -> "CursorPageDTO[LayoutSingleDB]":
        return await paginator_cursor(
            query=self._pagination_query(filters, session=session),
            params=filters,
            session=session,
            # sort=prepare_sort(filters.life_time_sort, self._collection),
            items_return_type=LayoutSingleDB,
        )

    def _pagination_query[DocType: Document, ProjectionModelType: BaseModel](
        self,
        filters: "LayoutSinglePaginationFiltersProtocol",
        *,
        session: "AsyncClientSession",
    ) -> FindManyQueryType[DocType, ProjectionModelType]:
        conditions: AnyList = []

        return self._collection.find_many(*conditions, session=session)
