from common.core.dtos import (
    HashDTO,
    HashOrNoneDTO,
    IdDTO,
    KeyDTO,
    LabelDTO,
    RequiredDTO,
)
from pydantic import Field

from src.application.enums import LayoutDataTypeEnum


class _LayoutSchemaBase(LabelDTO, RequiredDTO):
    default: str | None = Field(default=None)


# Update


class LayoutSchemaUpdateDTO(HashOrNoneDTO, _LayoutSchemaBase):
    pass


# Base


class LayoutSchemaBase(HashDTO, KeyDTO, _LayoutSchemaBase):
    type: LayoutDataTypeEnum


class LayoutSchemaDB(IdDTO, LayoutSchemaBase):
    pass


# Create


# TODO Убрать ключ и сделать его генерируемым
class LayoutSchemaCreateDTO(HashOrNoneDTO, KeyDTO, _LayoutSchemaBase):
    type: LayoutDataTypeEnum
