from typing import TYPE_CHECKING, Protocol

from abgroup_core.protocols import (
    AdderProtocol,
    GetterProtocol,
    PaginationCursorParamsProtocol,
    PaginationCursorProtocol,
    PaginationLiminOffsetProtocol,
    PaginationLimitOffsetParamsProtocol,
    PaginationPageProtocol,
    PaginationPagesParamsProtocol,
    SessionProtocol,
)

if TYPE_CHECKING:
    from pydantic import BaseModel


class _RepositoryProtocol[
    ReturnSchema: BaseModel,
    CreateSchema: BaseModel,
    # UpdateSchema: BaseModel,
    Session: SessionProtocol,
](
    GetterProtocol[ReturnSchema, Session],
    AdderProtocol[CreateSchema, ReturnSchema, Session],
    Protocol,
): ...


# TODO Реализовать после добавления методов update и create ко всем блокам
# class _ServiceProtocol[
#     ReturnSchema: BaseModel,
#     # CreateSchema: BaseModel,
#     # UpdateSchema: BaseModel,
# ](
#     # GetterProtocol[ReturnSchema, SessionProtocol],
#     # AdderProtocol[CreateSchema, ReturnSchema, SessionProtocol],
#     Protocol,
# ): ...


class _PaginationProtocol[
    PagesFiltersSchema: PaginationPagesParamsProtocol,
    LiminOffsetFiltersSchema: PaginationLimitOffsetParamsProtocol,
    CursorFiltersSchema: PaginationCursorParamsProtocol,
    ReturnSchema: BaseModel,
    Session: SessionProtocol,
](
    PaginationPageProtocol[
        PagesFiltersSchema,
        ReturnSchema,
        Session,
    ],
    PaginationLiminOffsetProtocol[
        LiminOffsetFiltersSchema,
        ReturnSchema,
        Session,
    ],
    PaginationCursorProtocol[
        CursorFiltersSchema,
        ReturnSchema,
        Session,
    ],
    Protocol,
): ...


class _GetWithLayersProtocol[
    FilterProtocol,
    ReturnSchema: BaseModel,
    Session: SessionProtocol,
](Protocol):
    async def get_with_layers(
        self, _id: str, filters: FilterProtocol, *, session: Session
    ) -> ReturnSchema: ...
