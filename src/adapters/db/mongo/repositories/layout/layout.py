from typing import TYPE_CHECKING

from common.core.custom_types import AnyList
from common.core.enums import LifeStatusEnum
from common.core.exceptions import NoContentError
from common.mongo import (
    DeleteSoftMixin,
    GetMixin,
    KeysEnum,
    ProjectionID,
    convert_to_dto,
    convert_to_id,
    paginator_cursor,
    paginator_limit_offset,
    paginator_pages,
    # prepare_sort,
)

from src.adapters.db.mongo.projections import LayoutShortProjection
from src.application.dtos.db import LayoutDB, LayoutWithBlocks
from src.application.dtos.db.layout import LayoutFullLinks, LayoutShortDTO

if TYPE_CHECKING:
    from beanie import Document
    from beanie.odm.queries.find import FindMany
    from common.core.dtos.pagination import (
        CursorPageDTO,
        LimitOffsetPageDTO,
        PagesPageDTO,
    )
    from pydantic import BaseModel
    from pymongo.asynchronous.client_session import AsyncClientSession

    from src.application.protocols import (
        LayoutShortCursorFiltersProtocol,
        LayoutShortFiltersProtocol,
        LayoutShortLimitOffsetFiltersProtocol,
        LayoutShortPagesFiltersProtocol,
    )

type FindManyQueryType[DocType, ProjectionModelType] = (
    FindMany[DocType] | FindMany[ProjectionModelType]
)


class LayoutRepository(GetMixin[LayoutDB], DeleteSoftMixin):
    async def get_all_pages(
        self,
        filters: "LayoutShortPagesFiltersProtocol",
        *,
        session: "AsyncClientSession",
    ) -> "PagesPageDTO[LayoutShortDTO]":
        return await paginator_pages(
            query=self._pagination_query(filters, session=session),
            params=filters,
            session=session,
            # sort=prepare_sort(filters.life_time_sort, self._collection),
            items_return_type=LayoutShortDTO,
            projection_model=LayoutShortProjection,
        )

    async def get_all_limit_offset(
        self,
        filters: "LayoutShortLimitOffsetFiltersProtocol",
        *,
        session: "AsyncClientSession",
    ) -> "LimitOffsetPageDTO[LayoutShortDTO]":
        return await paginator_limit_offset(
            query=self._pagination_query(filters, session=session),
            params=filters,
            session=session,
            # sort=prepare_sort(filters.life_time_sort, self._collection),
            items_return_type=LayoutShortDTO,
            projection_model=LayoutShortProjection,
        )

    async def get_all_cursor(
        self,
        filters: "LayoutShortCursorFiltersProtocol",
        *,
        session: "AsyncClientSession",
    ) -> "CursorPageDTO[LayoutShortDTO]":
        return await paginator_cursor(
            query=self._pagination_query(filters, session=session),
            params=filters,
            session=session,
            # sort=prepare_sort(filters.life_time_sort, self._collection),
            items_return_type=LayoutShortDTO,
            projection_model=LayoutShortProjection,
        )

    def _pagination_query[DocType: Document, ProjectionModelType: BaseModel](
        self,
        filters: "LayoutShortFiltersProtocol",
        *,
        session: "AsyncClientSession",
    ) -> FindManyQueryType[DocType, ProjectionModelType]:
        conditions: AnyList = []

        if filters.status:
            conditions.append(self._collection.status == filters.status)
        else:
            conditions.append(
                self._collection.status == LifeStatusEnum.published
            )

        return self._collection.find_many(*conditions, session=session)

    async def get_full_links(
        self,
        _id: str,
        *,
        session: "AsyncClientSession",
        nesting_depths_per_field: dict[str, int] | None = None,
    ) -> LayoutFullLinks:
        if nesting_depths_per_field is None:
            nesting_depths_per_field = {
                "card": 1,
                "singles": 1,
                "tables": 1,
                "messages": 1,
            }
        document = await self._collection.find_one(
            {KeysEnum.id: convert_to_id(_id)},
            session=session,
            fetch_links=True,
            nesting_depths_per_field=nesting_depths_per_field,
        )
        if not document:
            raise NoContentError
        return convert_to_dto(document, LayoutFullLinks, is_replace_links=True)

    async def get_by_key(
        self,
        key: str,
        *,
        session: "AsyncClientSession",
        nesting_depths_per_field: dict[str, int] | None = None,
    ) -> "LayoutWithBlocks":
        conditions = [
            self._collection.key == key,
            self._collection.status == LifeStatusEnum.published,
        ]
        if nesting_depths_per_field is None:
            nesting_depths_per_field = {
                "card": 0,
                "singles": 1,
                "tables": 1,
                "messages": 1,
            }
        document = await self._collection.find_one(
            *conditions,
            session=session,
            fetch_links=True,
            nesting_depths_per_field=nesting_depths_per_field,
        )
        if not document:
            raise NoContentError
        return convert_to_dto(document, LayoutWithBlocks, is_replace_links=True)

    async def get_ids_by(
        self, key: str, *, session: "AsyncClientSession"
    ) -> list[str]:
        documents = await self._collection.find_many(
            {self._collection.key: key},
            session=session,
            projection_model=ProjectionID,
        ).to_list()
        if not documents:
            raise NoContentError
        return [document.id for document in documents]
