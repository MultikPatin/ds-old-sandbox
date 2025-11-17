from typing import Any

from common.core.custom_types import AnyDict
from common.core.dtos import (
    CreatedDTO,
    DescriptionDTO,
    KeyDTO,
    LabelDTO,
    LifeStatusDTO,
    OptionsDTO,
    UpdatedDTO,
)
from common.mongo import IDProjection
from pydantic import BaseModel, field_validator


class LayoutShortProjection(
    IDProjection, KeyDTO, LabelDTO, CreatedDTO, UpdatedDTO, DescriptionDTO
):
    pass


class InputCardProjection(
    IDProjection, LifeStatusDTO, UpdatedDTO, OptionsDTO, CreatedDTO
):
    card: list[AnyDict] | None
    layout: str

    @field_validator("layout", mode="before")
    @classmethod
    def convert_layout(cls, value: Any) -> str:
        return str(value)


class InputLayoutProjection(BaseModel):
    layout: str

    @field_validator("layout", mode="before")
    @classmethod
    def convert_layout(cls, value: Any) -> str:
        return str(value)
