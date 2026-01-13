from abgroup_core.custom_types import AnyDict, AnyMatrix
from abgroup_fastapi.schemas import (
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
