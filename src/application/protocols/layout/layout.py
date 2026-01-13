from typing import TYPE_CHECKING, Protocol

from abgroup_core.enums import LifeStatusEnum
from abgroup_core.protocols import (
    DeleterSoftProtocol,
    GetterProtocol,
    PaginationCursorParamsProtocol,
    PaginationCursorProtocol,
    PaginationLiminOffsetProtocol,
    PaginationLimitOffsetParamsProtocol,
    PaginationPageProtocol,
    PaginationPagesParamsProtocol,
    SessionProtocol,
)

from src.application.dtos.db import LayoutDB, LayoutShortDTO

if TYPE_CHECKING:
    from src.application.dtos import LayoutWithBlockLayersDTO
    from src.application.dtos.db.layout import LayoutFullLinks, LayoutWithBlocks
    from src.application.enums import LayoutLayersEnum


class LayoutFiltersProtocol(Protocol):
    include_schema_layer: bool
    include_validation_layer: bool
    include_style_layer: bool
    include_default_layer: bool

    @property
    def excluded_layers(self) -> tuple["LayoutLayersEnum", ...]: ...


class LayoutShortFiltersProtocol(Protocol):
    # TODO заменить на протоколы
    status: LifeStatusEnum | None


class LayoutShortPagesFiltersProtocol(
    LayoutShortFiltersProtocol,
    PaginationPagesParamsProtocol,
    Protocol,
): ...


class LayoutShortLimitOffsetFiltersProtocol(
    LayoutShortFiltersProtocol,
    PaginationLimitOffsetParamsProtocol,
    Protocol,
): ...


class LayoutShortCursorFiltersProtocol(
    LayoutShortFiltersProtocol,
    PaginationCursorParamsProtocol,
    Protocol,
): ...


class _GetIdsBy[Session: SessionProtocol](Protocol):
    async def get_ids_by(self, key: str, *, session: Session) -> list[str]: ...


class _LayoutShortProtocol[Session: SessionProtocol](
    PaginationPageProtocol[
        LayoutShortPagesFiltersProtocol,
        LayoutShortDTO,
        Session,
    ],
    PaginationLiminOffsetProtocol[
        LayoutShortLimitOffsetFiltersProtocol,
        LayoutShortDTO,
        Session,
    ],
    PaginationCursorProtocol[
        LayoutShortCursorFiltersProtocol,
        LayoutShortDTO,
        Session,
    ],
    Protocol,
): ...


class LayoutServiceProtocol(
    GetterProtocol[LayoutDB, SessionProtocol],
    DeleterSoftProtocol[SessionProtocol],
    _GetIdsBy[SessionProtocol],
    _LayoutShortProtocol[SessionProtocol],
    Protocol,
):
    async def get_with_layers_by_key(
        self,
        key: str,
        filters: "LayoutFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "LayoutWithBlockLayersDTO": ...
    async def get_with_layers(
        self,
        _id: str,
        filters: "LayoutFiltersProtocol",
        *,
        session: SessionProtocol,
    ) -> "LayoutWithBlockLayersDTO": ...
    async def get_by_input(
        self,
        _id: str,
        filters: "LayoutFiltersProtocol",
        *,
        session: SessionProtocol,
    ) -> "LayoutWithBlockLayersDTO": ...
    async def get_full_links(
        self, _id: str, *, session: SessionProtocol
    ) -> "LayoutFullLinks": ...


class LayoutRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[LayoutDB, Session],
    DeleterSoftProtocol[Session],
    _GetIdsBy[Session],
    _LayoutShortProtocol[Session],
    Protocol,
):
    async def get_by_key(
        self,
        key: str,
        *,
        session: Session,
        nesting_depths_per_field: dict[str, int] | None = None,
    ) -> "LayoutWithBlocks": ...
    async def get_full_links(
        self,
        _id: str,
        *,
        session: Session,
        nesting_depths_per_field: dict[str, int] | None = None,
    ) -> "LayoutFullLinks": ...
