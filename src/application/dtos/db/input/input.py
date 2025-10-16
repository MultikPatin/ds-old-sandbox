from common.core.custom_types import AnyDict
from common.core.dtos import (
    CreatedDTO,
    IdDTO,
    LifeStatusDTO,
    OptionsDTO,
    UpdatedDTO,
)
from pydantic import BaseModel, Field

from .blocks import (
    InputSingleCreateDTO,
    InputSingleDB,
    InputSingleUpdateDTO,
    InputTableCreateDTO,
    InputTableFullLinks,
    InputTableInMatrix,
    InputTableUpdateDTO,
)


class InputCreateDTO(BaseModel):
    layout_id: str
    singles: list[InputSingleCreateDTO] | None = Field(default=None)
    tables: list[InputTableCreateDTO] | None = Field(default=None)


class InputUpdateDTO(
    IdDTO,
    LifeStatusDTO,
    UpdatedDTO,
    OptionsDTO,
):
    layout_id: str | None = Field(default=None)
    card: list[AnyDict] | None = Field(default=None)
    singles: list[InputSingleUpdateDTO] | None = Field(default=None)
    tables: list[InputTableUpdateDTO] | None = Field(default=None)


class InputBase(
    LifeStatusDTO,
    OptionsDTO,
    CreatedDTO,
    UpdatedDTO,
):
    card: list[AnyDict] | None = Field(default=None)


class InputDB(IdDTO, InputBase):
    pass


class InputWithTableInMatrix(InputDB):
    singles: list[InputSingleDB] | None = Field(default=None)
    tables: list[InputTableInMatrix] | None = Field(default=None)


class InputFullLinks(IdDTO, InputBase):
    singles: list[InputSingleDB] | None = Field(default=None)
    tables: list[InputTableFullLinks] | None = Field(default=None)
