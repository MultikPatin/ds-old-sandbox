from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from pydantic import BaseModel

    from common.core.dtos.pagination import (
        CursorPageDTO,
        LimitOffsetPageDTO,
        PagesPageDTO,
    )

    from .session import SessionProtocol


class PaginationPagesParamsProtocol(Protocol):
    number: int
    size: int


class PaginationLimitOffsetParamsProtocol(Protocol):
    limit: int
    offset: int


class PaginationCursorParamsProtocol(Protocol):
    cursor: str | None
    size: int


class PaginationPageProtocol[
    FiltersSchema: "PaginationPagesParamsProtocol",
    ReturnSchema: "BaseModel",
    Session: "SessionProtocol",
](Protocol):
    async def get_all_pages(
        self,
        filters: FiltersSchema,
        *,
        session: Session,
    ) -> "PagesPageDTO[ReturnSchema]": ...


class PaginationLiminOffsetProtocol[
    FiltersSchema: "PaginationLimitOffsetParamsProtocol",
    ReturnSchema: "BaseModel",
    Session: "SessionProtocol",
](Protocol):
    async def get_all_limit_offset(
        self,
        filters: FiltersSchema,
        *,
        session: Session,
    ) -> "LimitOffsetPageDTO[ReturnSchema]": ...


class PaginationCursorProtocol[
    FiltersSchema: "PaginationCursorParamsProtocol",
    ReturnSchema: "BaseModel",
    Session: "SessionProtocol",
](Protocol):
    async def get_all_cursor(
        self,
        filters: FiltersSchema,
        *,
        session: Session,
    ) -> "CursorPageDTO[ReturnSchema]": ...
