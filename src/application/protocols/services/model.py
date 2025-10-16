from typing import Protocol

from common.core.protocols import (
    PaginationCursorProtocol,
    PaginationLiminOffsetProtocol,
    PaginationPageProtocol,
    SessionProtocol,
)

from src.application.dtos.db.model import ModelDB, ModelWithPublishedLayoutID
from src.application.dtos.filters import ModelFilters


class ModelServiceProtocol(
    PaginationPageProtocol[
        ModelFilters,
        ModelWithPublishedLayoutID,
        SessionProtocol,
    ],
    PaginationLiminOffsetProtocol[
        ModelFilters,
        ModelWithPublishedLayoutID,
        SessionProtocol,
    ],
    PaginationCursorProtocol[
        ModelFilters,
        ModelWithPublishedLayoutID,
        SessionProtocol,
    ],
    Protocol,
):
    async def get_by_layout_id(
        self, _id: str, *, session: SessionProtocol | None = None
    ) -> ModelDB: ...
