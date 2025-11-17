from common.core.custom_types import AnyDict
from common.core.dtos import HashDTO, IdDTO, OptionsDTO
from pydantic import Field

from src.application.enums import LayoutStyleType


class _LayoutStyleBase(OptionsDTO):
    type: LayoutStyleType = Field(default=LayoutStyleType.default)
    dimension: AnyDict | None = Field(default=None)
    decimal_places: int | None = Field(default=None)
    postfix: str | None = Field(default=None)
    prefix: str | None = Field(default=None)


# Update


class LayoutStyleUpdateDTO(_LayoutStyleBase):
    pass


# Base


class LayoutStyleBase(HashDTO, _LayoutStyleBase):
    pass


class LayoutStyleDB(IdDTO, LayoutStyleBase):
    pass


# Create


class LayoutStyleCreateDTO(_LayoutStyleBase):
    pass
