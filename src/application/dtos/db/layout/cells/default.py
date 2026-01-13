from abgroup_core.dtos import (
    HashDTO,
    HashOrNoneDTO,
    IdDTO,
)
from pydantic import BaseModel, Field


class _LayoutDefaultBase(BaseModel):
    value: str | None = Field(default=None)


# Update


class LayoutDefaultUpdateDTO(HashOrNoneDTO, _LayoutDefaultBase):
    pass


# Base


class LayoutDefaultBase(HashDTO, _LayoutDefaultBase):
    pass


class LayoutDefaultDB(IdDTO, _LayoutDefaultBase):
    pass


# Create


class LayoutDefaultCreateDTO(HashOrNoneDTO, _LayoutDefaultBase):
    pass
