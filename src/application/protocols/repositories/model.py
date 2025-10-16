from typing import Protocol

from common.core.protocols import (
    GetterProtocol,
    PaginationCursorProtocol,
    PaginationLiminOffsetProtocol,
    PaginationPageProtocol,
    SessionProtocol,
)

from src.application.dtos.db.model import ModelDB, ModelWithPublishedLayoutID
from src.application.dtos.filters import ModelFilters


class ModelRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[ModelDB, Session],
    PaginationPageProtocol[
        ModelFilters,
        ModelWithPublishedLayoutID,
        Session,
    ],
    PaginationLiminOffsetProtocol[
        ModelFilters,
        ModelWithPublishedLayoutID,
        Session,
    ],
    PaginationCursorProtocol[
        ModelFilters,
        ModelWithPublishedLayoutID,
        Session,
    ],
    Protocol,
): ...
