from typing import Protocol

from common.core.protocols import (
    PaginationCursorProtocol,
    PaginationLiminOffsetProtocol,
    PaginationPageProtocol,
    SessionProtocol,
)

from src.application.dtos.db.input import InputCardDB
from src.application.dtos.filters import InputCardFilters


class InputCardServiceProtocol(
    PaginationPageProtocol[
        InputCardFilters,
        InputCardDB,
        SessionProtocol,
    ],
    PaginationLiminOffsetProtocol[
        InputCardFilters,
        InputCardDB,
        SessionProtocol,
    ],
    PaginationCursorProtocol[
        InputCardFilters,
        InputCardDB,
        SessionProtocol,
    ],
    Protocol,
): ...
