from typing import Protocol

from common.core.protocols import (
    AdderProtocol,
    GetterProtocol,
    SessionProtocol,
)

from src.application.dtos.db.layout import (
    LayoutSingleCreate,
    LayoutSingleDB,
    LayoutTableCreate,
    LayoutTableDB,
)


class LayoutSingleRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[LayoutSingleDB, Session],
    AdderProtocol[LayoutSingleCreate, LayoutSingleDB, Session],
    Protocol,
): ...


class LayoutTableRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[LayoutTableDB, Session],
    AdderProtocol[LayoutTableCreate, LayoutTableDB, Session],
    Protocol,
): ...
