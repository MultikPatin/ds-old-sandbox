from typing import Protocol

from abgroup_core.protocols import (
    PaginationCursorParamsProtocol,
    PaginationLimitOffsetParamsProtocol,
    PaginationPagesParamsProtocol,
    SessionProtocol,
)

from src.application.dtos.db import LayoutMessageCreateDTO, LayoutMessageDB

from ._base import _PaginationProtocol, _RepositoryProtocol, _ServiceProtocol


class LayoutMassagePaginationFiltersProtocol(Protocol):
    pass


class LayoutMassagePagesFiltersProtocol(
    LayoutMassagePaginationFiltersProtocol,
    PaginationPagesParamsProtocol,
    Protocol,
): ...


class LayoutMassageLimitOffsetFiltersProtocol(
    LayoutMassagePaginationFiltersProtocol,
    PaginationLimitOffsetParamsProtocol,
    Protocol,
): ...


class LayoutMassageCursorFiltersProtocol(
    LayoutMassagePaginationFiltersProtocol,
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
        LayoutMassagePagesFiltersProtocol,
        LayoutMassageLimitOffsetFiltersProtocol,
        LayoutMassageCursorFiltersProtocol,
        LayoutMessageDB,
        Session,
    ],
    Protocol,
): ...


class LayoutMessageServiceProtocol(
    _ServiceProtocol[
        LayoutMessageDB,
        # LayoutMessageCreateDTO,
        # Session,
    ],
    _PaginationProtocol[
        LayoutMassagePagesFiltersProtocol,
        LayoutMassageLimitOffsetFiltersProtocol,
        LayoutMassageCursorFiltersProtocol,
        LayoutMessageDB,
        SessionProtocol,
    ],
    Protocol,
): ...
