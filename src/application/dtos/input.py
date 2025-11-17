from common.core.custom_types import AnyMatrix
from pydantic import Field

from .db import InputDB, InputSingleDB, InputTableDB


class InputTableWithValuesDTO(InputTableDB):
    values: AnyMatrix


class InputWithValuesDTO(InputDB):
    singles: list[InputSingleDB] | None = Field(default=None)
    tables: list[InputTableWithValuesDTO] | None = Field(default=None)
