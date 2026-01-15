from typing import Protocol

from abgroup_core.protocols import (
    PaginationCursorParamsProtocol,
    PaginationLimitOffsetParamsProtocol,
    PaginationPagesParamsProtocol,
    SessionProtocol,
)

from src.application.dtos.db import (
    LayoutTableCreateDTO,
    LayoutTableDB,
)

from ._base import _PaginationProtocol, _RepositoryProtocol, _ServiceProtocol


class LayoutTablePaginationFiltersProtocol(Protocol):
    pass


class LayoutTablePagesFiltersProtocol(
    LayoutTablePaginationFiltersProtocol,
    PaginationPagesParamsProtocol,
    Protocol,
): ...


class LayoutTableLimitOffsetFiltersProtocol(
    LayoutTablePaginationFiltersProtocol,
    PaginationLimitOffsetParamsProtocol,
    Protocol,
): ...


class LayoutTableCursorFiltersProtocol(
    LayoutTablePaginationFiltersProtocol,
    PaginationCursorParamsProtocol,
    Protocol,
): ...


class LayoutTableRepositoryProtocol[Session: SessionProtocol](
    _RepositoryProtocol[
        LayoutTableDB,
        LayoutTableCreateDTO,
        Session,
    ],
    _PaginationProtocol[
        LayoutTablePagesFiltersProtocol,
        LayoutTableLimitOffsetFiltersProtocol,
        LayoutTableCursorFiltersProtocol,
        LayoutTableDB,
        Session,
    ],
    Protocol,
): ...


class LayoutTableServiceProtocol(
    _ServiceProtocol[
        LayoutTableDB,
        # LayoutTableCreateDTO,
        # Session,
    ],
    _PaginationProtocol[
        LayoutTablePagesFiltersProtocol,
        LayoutTableLimitOffsetFiltersProtocol,
        LayoutTableCursorFiltersProtocol,
        LayoutTableDB,
        SessionProtocol,
    ],
    Protocol,
): ...
