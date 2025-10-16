from common.core.custom_types import AnyList, AnyMatrix
from common.fastapi.schemas import BsonIDSchema, KeySchema
from pydantic import BaseModel


class InputTableChunkUpdate(BsonIDSchema):
    values: AnyList


class InputTableChunkResponse(BsonIDSchema):
    values: AnyList


class InputTableCreate(KeySchema):
    columns: list[str]
    values: AnyMatrix


class InputTableUpdateSchema(BsonIDSchema):
    values: AnyMatrix


class InputTableBulkUpdate(BaseModel):
    items: list[InputTableUpdateSchema]


class InputTableResponse(BsonIDSchema, KeySchema):
    columns: list[str]
    chunks: list[InputTableChunkResponse]


class InputTableInMatrixResponse(BsonIDSchema, KeySchema):
    columns: list[str]
    values: AnyMatrix


class InputTableBulkResponse(BaseModel):
    items: list[InputTableResponse]
