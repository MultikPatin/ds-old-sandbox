from typing import Protocol

from abgroup_core.protocols import (
    PaginationCursorParamsProtocol,
    PaginationLimitOffsetParamsProtocol,
    PaginationPagesParamsProtocol,
    SessionProtocol,
)

from src.application.dtos.db import (
    LayoutSingleCreateDTO,
    LayoutSingleDB,
)

from ._base import _PaginationProtocol, _RepositoryProtocol, _ServiceProtocol


class LayoutSinglePaginationFiltersProtocol(Protocol):
    pass


class LayoutSinglePagesFiltersProtocol(
    LayoutSinglePaginationFiltersProtocol,
    PaginationPagesParamsProtocol,
    Protocol,
): ...


class LayoutSingleLimitOffsetFiltersProtocol(
    LayoutSinglePaginationFiltersProtocol,
    PaginationLimitOffsetParamsProtocol,
    Protocol,
): ...


class LayoutSingleCursorFiltersProtocol(
    LayoutSinglePaginationFiltersProtocol,
    PaginationCursorParamsProtocol,
    Protocol,
): ...


class LayoutSingleRepositoryProtocol[Session: SessionProtocol](
    _RepositoryProtocol[
        LayoutSingleDB,
        LayoutSingleCreateDTO,
        Session,
    ],
    _PaginationProtocol[
        LayoutSinglePagesFiltersProtocol,
        LayoutSingleLimitOffsetFiltersProtocol,
        LayoutSingleCursorFiltersProtocol,
        LayoutSingleDB,
        Session,
    ],
    Protocol,
): ...


class LayoutSingleServiceProtocol(
    _ServiceProtocol[
        LayoutSingleDB,
        # LayoutSingleCreateDTO,
        # SessionProtocol,
    ],
    _PaginationProtocol[
        LayoutSinglePagesFiltersProtocol,
        LayoutSingleLimitOffsetFiltersProtocol,
        LayoutSingleCursorFiltersProtocol,
        LayoutSingleDB,
        SessionProtocol,
    ],
    Protocol,
): ...
