from common.core.custom_types import AnyDict, AnyMatrix
from common.fastapi.schemas import (
    BsonIDSchema,
    KeySchema,
)


class InputSingleResponse(
    BsonIDSchema,
    KeySchema,
):
    values: AnyDict


class InputTableResponse(
    BsonIDSchema,
    KeySchema,
):
    values: AnyMatrix
