from typing import Protocol

from abgroup_core.protocols import (
    PaginationCursorParamsProtocol,
    PaginationLimitOffsetParamsProtocol,
    PaginationPagesParamsProtocol,
    SessionProtocol,
)

from src.application.dtos import LayoutTableWithLayersDTO
from src.application.dtos.db import (
    LayoutTableCreateDTO,
    LayoutTableDB,
)
from src.application.protocols.layout.filters import (
    LayersFetcherFiltersProtocol,
)

from ._base import (
    _GetWithLayersProtocol,
    _PaginationProtocol,
    _RepositoryProtocol,
)


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
    # TODO перенести в _ServiceProtocol при реализации в остальных блоках
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
    # TODO перенести в _ServiceProtocol при реализации в остальных блоках
    _GetWithLayersProtocol[
        LayersFetcherFiltersProtocol,
        LayoutTableWithLayersDTO,
        SessionProtocol,
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
