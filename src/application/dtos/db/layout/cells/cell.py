from typing import Any

from common.core.dtos import (
    HashDTO,
    IdDTO,
    KeyDTO,
    LabelDTO,
    RequiredDTO,
)
from pydantic import Field

from src.application.enums import LayoutDataType


class _LayoutSchemaBase(LabelDTO, RequiredDTO):
    default: Any = Field(default=None)


# Update


class LayoutSchemaUpdateDTO(_LayoutSchemaBase):
    pass


# Base


class LayoutSchemaBase(HashDTO, KeyDTO, _LayoutSchemaBase):
    type: LayoutDataType


class LayoutSchemaDB(IdDTO, LayoutSchemaBase):
    pass


# Create


class LayoutSchemaCreateDTO(KeyDTO, _LayoutSchemaBase):
    type: LayoutDataType
