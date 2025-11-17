from common.core.dtos import IdDTO, KeyDTO, OptionsDTO
from pydantic import Field

from src.application.custom_types import NestingType


class _LayoutTableBase(OptionsDTO):
    schemas: list[list[str]] | None = Field(default=None)
    validations: list[list[str]] | None = Field(default=None)
    styles: list[list[str]] | None = Field(default=None)

    static: bool = Field(default=False)
    nesting: NestingType = Field(default=None)


# Update


class LayoutTableUpdateDTO(_LayoutTableBase):
    pass


# Base


class LayoutTableBase(KeyDTO, _LayoutTableBase):
    pass


class LayoutTableDB(IdDTO, LayoutTableBase):
    pass


# Create


class LayoutTableCreateDTO(LayoutTableBase):
    pass
