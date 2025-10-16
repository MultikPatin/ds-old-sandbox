from typing import Protocol

from common.core.protocols import (
    PaginationCursorProtocol,
    PaginationLiminOffsetProtocol,
    PaginationPageProtocol,
    SessionProtocol,
)

from src.application.dtos.db.input import InputCardDB
from src.application.dtos.filters import InputCardFilters


class InputCardRepositoryProtocol[Session: SessionProtocol](
    PaginationPageProtocol[InputCardFilters, InputCardDB, Session],
    PaginationLiminOffsetProtocol[InputCardFilters, InputCardDB, Session],
    PaginationCursorProtocol[InputCardFilters, InputCardDB, Session],
    Protocol,
): ...
