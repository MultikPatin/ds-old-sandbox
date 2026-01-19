from typing import Protocol

from abgroup_core.protocols import (
    AdderProtocol,
    GetterProtocol,
    PaginationCursorParamsProtocol,
    PaginationLimitOffsetParamsProtocol,
    PaginationPagesParamsProtocol,
    SessionProtocol,
    UpdaterProtocol,
)

from src.application.dtos import LayoutMessageCreate
from src.application.dtos.db import (
    LayoutMessageCreateDTO,
    LayoutMessageDB,
    LayoutMessageUpdateDTO,
)

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
    # TODO перенести в _ServiceProtocol при реализации в остальных блоках
    UpdaterProtocol[LayoutMessageUpdateDTO, LayoutMessageDB, Session],
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
    AdderProtocol[LayoutMessageCreate, LayoutMessageDB, SessionProtocol],
    UpdaterProtocol[LayoutMessageUpdateDTO, LayoutMessageDB, SessionProtocol],
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
