from common.fastapi.schemas import (
    BsonIDSchema,
    KeySchema,
    LabelSchema,
    RequiredSchema,
)
from pydantic import Field

from src.application.enums import LayoutDataTypeEnum, LayoutStyleTypeEnum


class LayoutStyleResponse(BsonIDSchema):
    type: LayoutStyleTypeEnum
    width: int | None = Field(default=None)
    decimal_places: int | None = Field(default=None)
    postfix: str | None = Field(default=None)
    prefix: str | None = Field(default=None)


class LayoutValidationResponse(BsonIDSchema):
    gt: int | None = Field(default=None)
    ge: int | None = Field(default=None)
    lt: int | None = Field(default=None)
    le: int | None = Field(default=None)
    max_digits: int | None = Field(default=None)
    decimal_places: int | None = Field(default=None)
    min_length: int | None = Field(default=None)
    max_length: int | None = Field(default=None)


class LayoutSchemaResponse(
    BsonIDSchema, KeySchema, LabelSchema, RequiredSchema
):
    default: str | None = Field(default=None)
    type: LayoutDataTypeEnum
