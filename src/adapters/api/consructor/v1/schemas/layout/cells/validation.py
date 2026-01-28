from abgroup_fastapi.schemas import BsonIDSchema, OptionsSchema
from pydantic import Field


class _LayoutValidation(OptionsSchema):
    gt: int | None = Field(default=None)
    ge: int | None = Field(default=None)
    lt: int | None = Field(default=None)
    le: int | None = Field(default=None)
    max_digits: int | None = Field(default=None)
    decimal_places: int | None = Field(default=None)
    min_length: int | None = Field(default=None)
    max_length: int | None = Field(default=None)


class LayoutValidationUpdateRequest(_LayoutValidation):
    pass


class LayoutValidationResponse(BsonIDSchema, _LayoutValidation):
    pass


class LayoutValidationCreateRequest(_LayoutValidation):
    pass
