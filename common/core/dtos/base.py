from typing import Any

from pydantic import BaseModel, Field, field_validator

from common.core.custom_types import AnyDict


class IdDTO(BaseModel):
    id: str

    @field_validator("id", mode="before")
    @classmethod
    def convert_id(cls, value: Any) -> str:
        if isinstance(value, str):
            return value
        # TODO Добавить ошибку преобразования в строку
        return str(value)


class KeyDTO(BaseModel):
    key: str = Field(min_length=1, max_length=64)


class ValueDTO(BaseModel):
    value: str = Field(min_length=1, max_length=255)


class LabelDTO(BaseModel):
    label: str = Field(min_length=1, max_length=255)


class TitleDTO(BaseModel):
    title: str = Field(min_length=1, max_length=255)


class DescriptionDTO(BaseModel):
    description: str | None = Field(default=None)


class RefCountDTO(BaseModel):
    ref_count: int = Field(default=0)


class HashDTO(RefCountDTO):
    hash: str = Field(min_length=8, max_length=255)


class OptionsDTO(BaseModel):
    options: AnyDict | None = Field(default=None)


class RequiredDTO(BaseModel):
    required: bool = Field(default=False)
