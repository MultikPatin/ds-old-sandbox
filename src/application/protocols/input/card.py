from datetime import datetime
from typing import Protocol

from abgroup_core.enums import (
    CreateUpdateEnum,
    LifeActionTimeSortEnum,
    LifeStatusEnum,
)
from abgroup_core.protocols import (
    PaginationCursorParamsProtocol,
    PaginationCursorProtocol,
    PaginationLiminOffsetProtocol,
    PaginationLimitOffsetParamsProtocol,
    PaginationPageProtocol,
    PaginationPagesParamsProtocol,
    SessionProtocol,
)

from src.application.dtos.db import InputCardDTO


class InputCardInRichFiltersProtocol(Protocol):
    layout_ids: list[str]
    layout_key: str


class InputCardFiltersProtocol(InputCardInRichFiltersProtocol, Protocol):
    # TODO заменить на протоколы
    life_time_sort: LifeActionTimeSortEnum | None
    status: LifeStatusEnum | None
    period_start: datetime | None
    period_end: datetime | None
    life_action_field: CreateUpdateEnum


class InputCardPagesFiltersProtocol(
    InputCardFiltersProtocol,
    PaginationPagesParamsProtocol,
    Protocol,
): ...


class InputCardLimitOffsetFiltersProtocol(
    InputCardFiltersProtocol,
    PaginationLimitOffsetParamsProtocol,
    Protocol,
): ...


class InputCardCursorFiltersProtocol(
    InputCardFiltersProtocol,
    PaginationCursorParamsProtocol,
    Protocol,
): ...


class _InputCardProtocol[Session: SessionProtocol](
    PaginationPageProtocol[
        InputCardPagesFiltersProtocol,
        InputCardDTO,
        Session,
    ],
    PaginationLiminOffsetProtocol[
        InputCardLimitOffsetFiltersProtocol,
        InputCardDTO,
        Session,
    ],
    PaginationCursorProtocol[
        InputCardCursorFiltersProtocol,
        InputCardDTO,
        Session,
    ],
    Protocol,
): ...


class InputCardServiceProtocol(
    _InputCardProtocol[SessionProtocol],
    Protocol,
): ...


class InputCardRepositoryProtocol[Session: SessionProtocol](
    _InputCardProtocol[Session],
    Protocol,
): ...
