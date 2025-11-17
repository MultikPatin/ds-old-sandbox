from typing import Protocol

from common.core.protocols import (
    AdderProtocol,
    GetterProtocol,
    SessionProtocol,
)

from src.application.dtos.db import (
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
