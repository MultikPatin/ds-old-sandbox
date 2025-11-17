from common.core.dtos import HashDTO, IdDTO, OptionsDTO
from pydantic import Field


class _LayoutValidationBase(OptionsDTO):
    gt: int | None = Field(default=None)
    ge: int | None = Field(default=None)
    lt: int | None = Field(default=None)
    le: int | None = Field(default=None)
    max_digits: int | None = Field(default=None)
    decimal_places: int | None = Field(default=None)
    min_length: int | None = Field(default=None)
    max_length: int | None = Field(default=None)


# Update


class LayoutValidationUpdateDTO(_LayoutValidationBase):
    pass


# Base


class LayoutValidationBase(HashDTO, _LayoutValidationBase):
    pass


class LayoutValidationDB(IdDTO, LayoutValidationBase):
    pass


# Create


class LayoutValidationCreateDTO(_LayoutValidationBase):
    pass
