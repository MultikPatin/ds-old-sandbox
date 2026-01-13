from abgroup_core.custom_types import AnyDict, AnyMatrix
from abgroup_core.dtos import KeyDTO
from pydantic import BaseModel, Field

from .db import (
    InputDB,
    InputSingleDB,
    InputTableDB,
)


class InputTableWithValuesDTO(InputTableDB):
    values: AnyMatrix


class InputWithValuesDTO(InputDB):
    singles: list[InputSingleDB] | None = Field(default=None)
    tables: list[InputTableWithValuesDTO] | None = Field(default=None)


class InputTableCreateValuesDTO(KeyDTO):
    values: AnyMatrix


class InputSingleCreateValuesDTO(KeyDTO):
    values: AnyDict


class InputCreateValuesDTO(BaseModel):
    layout: str
    singles: list[InputSingleCreateValuesDTO] | None = Field(default=None)
    tables: list[InputTableCreateValuesDTO] | None = Field(default=None)
