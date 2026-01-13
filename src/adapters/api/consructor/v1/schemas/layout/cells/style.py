from abgroup_fastapi.schemas import BsonIDSchema, OptionsSchema
from pydantic import Field

from src.application.enums import LayoutStyleTypeEnum


class _LayoutStyle(OptionsSchema):
    type: LayoutStyleTypeEnum = Field(default=LayoutStyleTypeEnum.default)
    width: int | None = Field(default=None)
    decimal_places: int | None = Field(default=None)
    postfix: str | None = Field(default=None)
    prefix: str | None = Field(default=None)


class LayoutStyleUpdateRequest(_LayoutStyle):
    pass


class LayoutStyleResponse(BsonIDSchema, _LayoutStyle):
    pass


class LayoutStyleCreateRequest(_LayoutStyle):
    pass
