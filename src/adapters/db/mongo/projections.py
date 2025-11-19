from typing import Any

from beanie import Link
from bson import DBRef
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
from common.mongo import ProjectionID
from pydantic import BaseModel, field_validator


class LayoutShortProjection(
    ProjectionID, KeyDTO, LabelDTO, CreatedDTO, UpdatedDTO, DescriptionDTO
):
    pass


class InputCardProjection(
    ProjectionID, LifeStatusDTO, UpdatedDTO, OptionsDTO, CreatedDTO
):
    card: list[AnyDict] | None
    layout: str

    @field_validator("layout", mode="before")
    @classmethod
    def convert_layout(cls, value: Any) -> str:
        if isinstance(value, DBRef):
            return str(value.id)
        if isinstance(value, Link):
            return str(value.ref.id)
        return str(value)


class InputLayoutProjection(BaseModel):
    layout: str

    @field_validator("layout", mode="before")
    @classmethod
    def convert_layout(cls, value: Any) -> str:
        if isinstance(value, DBRef):
            return str(value.id)
        if isinstance(value, Link):
            return str(value.ref.id)
        return str(value)
