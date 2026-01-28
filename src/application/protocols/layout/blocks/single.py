from typing import Protocol

from abgroup_core.protocols import (
    PaginationCursorParamsProtocol,
    PaginationLimitOffsetParamsProtocol,
    PaginationPagesParamsProtocol,
    SessionProtocol,
)

from src.application.dtos import LayoutSingleWithLayersDTO
from src.application.dtos.db import (
    LayoutSingleCreateDTO,
    LayoutSingleDB,
)
from src.application.protocols.layout.filters import (
    LayersFetcherFiltersProtocol,
)

from ._base import (
    _GetWithLayersProtocol,
    _PaginationProtocol,
    _RepositoryProtocol,
)


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
    # TODO перенести в _ServiceProtocol при реализации в остальных блоках
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
    # TODO перенести в _ServiceProtocol при реализации в остальных блоках
    _GetWithLayersProtocol[
        LayersFetcherFiltersProtocol,
        LayoutSingleWithLayersDTO,
        SessionProtocol,
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
