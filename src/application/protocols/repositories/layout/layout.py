from typing import Protocol

from common.core.protocols import GetterProtocol, SessionProtocol

from src.application.dtos.db.layout import LayoutFullLinks


class LayoutRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[LayoutFullLinks, Session], Protocol
): ...
