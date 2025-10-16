from pydantic import BaseModel, Field

from common.core.constants import (
    ID_BSON_DESCRIPTION,
    ID_BSON_EXAMPLES,
    ID_BSON_MAX_LENGTH,
    ID_BSON_MIN_LENGTH,
    ID_BSON_PATTERN,
    ID_BSON_TITLE,
    ID_DEFAULT_ALIAS,
    ID_INTEGER_DESCRIPTION,
    ID_INTEGER_EXAMPLES,
    ID_INTEGER_MAX_VALUE,
    ID_INTEGER_MIN_VALUE,
    ID_INTEGER_TITLE,
    ID_UUID4_DESCRIPTION,
    ID_UUID4_EXAMPLES,
    ID_UUID4_MAX_LENGTH,
    ID_UUID4_MIN_LENGTH,
    ID_UUID4_PATTERN,
    ID_UUID4_TITLE,
)


class BsonIDSchema(BaseModel):
    id: str = Field(  # type: ignore
        alias=ID_DEFAULT_ALIAS,
        min_length=ID_BSON_MIN_LENGTH,
        max_length=ID_BSON_MAX_LENGTH,
        title=ID_BSON_TITLE,
        description=ID_BSON_DESCRIPTION,
        examples=ID_BSON_EXAMPLES,
        pattern=ID_BSON_PATTERN,
    )


class IntegerIDSchema(BaseModel):
    id: str = Field(  # type: ignore
        alias=ID_DEFAULT_ALIAS,
        ge=ID_INTEGER_MIN_VALUE,
        lt=ID_INTEGER_MAX_VALUE,
        title=ID_INTEGER_TITLE,
        description=ID_INTEGER_DESCRIPTION,
        examples=ID_INTEGER_EXAMPLES,
    )


class UUID4IDSchema(BaseModel):
    id: str = Field(  # type: ignore
        alias=ID_DEFAULT_ALIAS,
        min_length=ID_UUID4_MIN_LENGTH,
        max_length=ID_UUID4_MAX_LENGTH,
        title=ID_UUID4_TITLE,
        description=ID_UUID4_DESCRIPTION,
        examples=ID_UUID4_EXAMPLES,
        pattern=ID_UUID4_PATTERN,
    )
