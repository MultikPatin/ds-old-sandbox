from typing import TYPE_CHECKING, Protocol

from common.core.enums import LifeStatusEnum
from common.core.protocols import (
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

    @property
    def excluded_layers(self) -> tuple["LayoutLayersEnum", ...]: ...


class _GetFullLinks[Session: SessionProtocol](Protocol):
    async def get_full_links(
        self, _id: str, *, session: Session
    ) -> "LayoutFullLinks": ...


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
    _GetFullLinks[SessionProtocol],
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


class LayoutRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[LayoutDB, Session],
    DeleterSoftProtocol[Session],
    _GetFullLinks[Session],
    _GetIdsBy[Session],
    _LayoutShortProtocol[Session],
    Protocol,
):
    async def get_by_key(
        self, key: str, *, session: Session
    ) -> "LayoutWithBlocks": ...
