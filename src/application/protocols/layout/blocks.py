from typing import Protocol

from common.core.protocols import (
    AdderProtocol,
    GetterProtocol,
    SessionProtocol,
)

from src.application.dtos.db import (
    LayoutCardCreateDTO,
    LayoutCardDB,
    LayoutMessageCreateDTO,
    LayoutMessageDB,
    LayoutSingleCreateDTO,
    LayoutSingleDB,
    LayoutTableCreateDTO,
    LayoutTableDB,
)


class LayoutSingleRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[LayoutSingleDB, Session],
    AdderProtocol[LayoutSingleCreateDTO, LayoutSingleDB, Session],
    Protocol,
): ...


class LayoutTableRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[LayoutTableDB, Session],
    AdderProtocol[LayoutTableCreateDTO, LayoutTableDB, Session],
    Protocol,
): ...


class LayoutMessageRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[LayoutMessageDB, Session],
    AdderProtocol[LayoutMessageCreateDTO, LayoutMessageDB, Session],
    Protocol,
): ...


class LayoutCardRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[LayoutCardDB, Session],
    AdderProtocol[LayoutCardCreateDTO, LayoutCardDB, Session],
    Protocol,
):
    async def get_by_layout_id(
        self, layout_id: str, *, session: Session
    ) -> LayoutCardDB | None: ...
