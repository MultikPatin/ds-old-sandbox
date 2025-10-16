from typing import Protocol

from common.core.protocols import (
    AdderProtocol,
    GetterProtocol,
    SessionProtocol,
)

from src.application.dtos.db.reference import ReferenceCreate, ReferenceDB


class ReferenceRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[ReferenceDB, Session],
    AdderProtocol[ReferenceCreate, ReferenceDB, Session],
    Protocol,
): ...
