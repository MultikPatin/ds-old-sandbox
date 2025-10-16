from common.core.custom_types import AnyDict
from common.core.dtos import (
    CreatedDTO,
    IdDTO,
    LifeStatusDTO,
    OptionsDTO,
    UpdatedDTO,
)
from pydantic import Field


class InputCardDB(
    IdDTO,
    CreatedDTO,
    UpdatedDTO,
    LifeStatusDTO,
    OptionsDTO,
):
    # TODO Реализовать схему для карточки
    card: list[AnyDict] | None = Field(default=None)
