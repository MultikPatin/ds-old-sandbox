from typing import Protocol

from pydantic import BaseModel

from common.core.dtos import (
    CursorPageDTO,
    CursorParamsDTO,
    LimitOffsetPageDTO,
    LimitOffsetParamsDTO,
    PagesPageDTO,
    PagesParamsDTO,
)

from .session import SessionProtocol


class PaginationPageProtocol[
    FiltersSchema: BaseModel,
    ReturnSchema: BaseModel,
    Session: SessionProtocol,
](Protocol):
    async def get_all_like_pages(
        self,
        params: PagesParamsDTO,
        filters: FiltersSchema,
        *,
        session: Session | None = None,
    ) -> PagesPageDTO[ReturnSchema]: ...


class PaginationLiminOffsetProtocol[
    FiltersSchema: BaseModel,
    ReturnSchema: BaseModel,
    Session: SessionProtocol,
](Protocol):
    async def get_all_like_limit_offset(
        self,
        params: LimitOffsetParamsDTO,
        filters: FiltersSchema,
        *,
        session: Session | None = None,
    ) -> LimitOffsetPageDTO[ReturnSchema]: ...


class PaginationCursorProtocol[
    FiltersSchema: BaseModel,
    ReturnSchema: BaseModel,
    Session: SessionProtocol,
](Protocol):
    async def get_all_like_cursor(
        self,
        params: CursorParamsDTO,
        filters: FiltersSchema,
        *,
        session: Session | None = None,
    ) -> CursorPageDTO[ReturnSchema]: ...
