from typing import Any

from pydantic import BaseModel, Field, field_validator


class IDProjection(BaseModel):
    id: str = Field(validation_alias="_id")

    @field_validator("id", mode="before")
    @classmethod
    def convert_id(cls, value: Any) -> str:
        if isinstance(value, str):
            return value
        return str(value)
