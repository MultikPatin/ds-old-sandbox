from common.core.custom_types import AnyDict
from common.fastapi.schemas import BsonIDSchema, KeySchema
from pydantic import BaseModel


class InputSingleCreate(KeySchema):
    values: AnyDict


class InputSingleUpdateSchema(BsonIDSchema):
    values: AnyDict


class InputSingleBulkUpdateSchema(BaseModel):
    items: list[InputSingleUpdateSchema]


class InputSingleResponse(BsonIDSchema, InputSingleCreate):
    pass


class InputSingleBulkResponse(BaseModel):
    items: list[InputSingleResponse]
