from common.core.dtos import IdDTO, KeyDTO
from pydantic import BaseModel, Field


class _LayoutSingleBase(BaseModel):
    schemas: list[str] | None = Field(default=None)
    validations: list[str] | None = Field(default=None)
    styles: list[str] | None = Field(default=None)
    defaults: list[str] | None = Field(default=None)


# Update


class LayoutSingleUpdateDTO(_LayoutSingleBase):
    pass


# Base


class LayoutSingleBase(KeyDTO, _LayoutSingleBase):
    pass


class LayoutSingleDB(IdDTO, LayoutSingleBase):
    pass


# Create


class LayoutSingleCreateDTO(LayoutSingleBase):
    pass
