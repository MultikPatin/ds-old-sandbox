from typing import Protocol

from abgroup_core.protocols import (
    GetterProtocol,
    PaginationCursorParamsProtocol,
    PaginationLimitOffsetParamsProtocol,
    PaginationPagesParamsProtocol,
    SessionProtocol,
)

from src.application.dtos.db import LayoutMessageCreateDTO, LayoutMessageDB

from ._base import _PaginationProtocol, _RepositoryProtocol, _ServiceProtocol


class LayoutMessagePaginationFiltersProtocol(Protocol):
    pass


class LayoutMessagePagesFiltersProtocol(
    LayoutMessagePaginationFiltersProtocol,
    PaginationPagesParamsProtocol,
    Protocol,
): ...


class LayoutMessageLimitOffsetFiltersProtocol(
    LayoutMessagePaginationFiltersProtocol,
    PaginationLimitOffsetParamsProtocol,
    Protocol,
): ...


class LayoutMessageCursorFiltersProtocol(
    LayoutMessagePaginationFiltersProtocol,
    PaginationCursorParamsProtocol,
    Protocol,
): ...


class LayoutMessageRepositoryProtocol[Session: SessionProtocol](
    _RepositoryProtocol[
        LayoutMessageDB,
        LayoutMessageCreateDTO,
        Session,
    ],
    _PaginationProtocol[
        LayoutMessagePagesFiltersProtocol,
        LayoutMessageLimitOffsetFiltersProtocol,
        LayoutMessageCursorFiltersProtocol,
        LayoutMessageDB,
        Session,
    ],
    Protocol,
): ...


class LayoutMessageServiceProtocol(
    # TODO перенести в _ServiceProtocol при реализации в остальных блоках
    GetterProtocol[LayoutMessageDB, SessionProtocol],
    _ServiceProtocol[
        LayoutMessageDB,
        # LayoutMessageCreateDTO,
        # Session,
    ],
    _PaginationProtocol[
        LayoutMessagePagesFiltersProtocol,
        LayoutMessageLimitOffsetFiltersProtocol,
        LayoutMessageCursorFiltersProtocol,
        LayoutMessageDB,
        SessionProtocol,
    ],
    Protocol,
): ...
