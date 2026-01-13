from abgroup_core.custom_types import AnyDict
from abgroup_core.dtos import (
    CreatedDTO,
    IdDTO,
    LifeStatusDTO,
    OptionsDTO,
    UpdatedDTO,
)
from pydantic import BaseModel, Field

from .blocks import (
    InputSingleDB,
    InputSingleUpdateDTO,
    InputTableDB,
    InputTableUpdateDTO,
)


class _Base(LifeStatusDTO, UpdatedDTO, OptionsDTO):
    pass


class _Card(BaseModel):
    # TODO: Отрефакторить при переходе на работу через ячейки
    card: list[AnyDict] | None = Field(default=None)


# Card


class InputCardDTO(IdDTO, _Base, _Card, CreatedDTO):
    layout: str


# Update


class InputUpdateDTO(_Base, _Card):
    singles: list[InputSingleUpdateDTO] | None = Field(default=None)
    tables: list[InputTableUpdateDTO] | None = Field(default=None)


# Base


class InputBase(_Card, _Base, CreatedDTO):
    pass


class InputDB(IdDTO, InputBase):
    layout: str


class InputWithBlocks(InputDB):
    singles: list[InputSingleDB] | None = Field(default=None)
    tables: list[InputTableDB] | None = Field(default=None)


# Create


class InputCreateDTO(_Card, OptionsDTO):
    layout: str
    singles: list[str] | None = Field(default=None)
    tables: list[str] | None = Field(default=None)
