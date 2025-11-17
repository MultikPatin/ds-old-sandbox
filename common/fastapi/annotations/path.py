from typing import Any

from fastapi import Path, Query
from pydantic import Field

from common.core.constants import (
    ID_BSON_DESCRIPTION,
    ID_BSON_EXAMPLE,
    ID_BSON_EXAMPLES,
    ID_BSON_MAX_LENGTH,
    ID_BSON_MIN_LENGTH,
    ID_BSON_PATTERN,
    ID_BSON_TITLE,
    ID_DEFAULT_ALIAS,
    ID_INTEGER_DESCRIPTION,
    ID_INTEGER_EXAMPLE,
    ID_INTEGER_EXAMPLES,
    ID_INTEGER_MIN_LENGTH,
    ID_INTEGER_TITLE,
    ID_UUID4_DESCRIPTION,
    ID_UUID4_EXAMPLE,
    ID_UUID4_EXAMPLES,
    ID_UUID4_MAX_LENGTH,
    ID_UUID4_MIN_LENGTH,
    ID_UUID4_PATTERN,
    ID_UUID4_TITLE,
)
from common.core.enums import IDTypesEnum


def _dispatch_params(id_type: IDTypesEnum) -> dict[str, Any]:
    match id_type:
        case IDTypesEnum.bson:
            params = {
                "min_length": ID_BSON_MIN_LENGTH,
                "max_length": ID_BSON_MAX_LENGTH,
                "pattern": ID_BSON_PATTERN,
                "title": ID_BSON_TITLE,
                "description": ID_BSON_DESCRIPTION,
                "example": ID_BSON_EXAMPLE,
                "examples": ID_BSON_EXAMPLES,
            }
        case IDTypesEnum.integer:
            params = {
                "min_length": ID_INTEGER_MIN_LENGTH,
                "title": ID_INTEGER_TITLE,
                "description": ID_INTEGER_DESCRIPTION,
                "example": ID_INTEGER_EXAMPLE,
                "examples": ID_INTEGER_EXAMPLES,
            }
        case IDTypesEnum.uuid4:
            params = {
                "min_length": ID_UUID4_MIN_LENGTH,
                "max_length": ID_UUID4_MAX_LENGTH,
                "pattern": ID_UUID4_PATTERN,
                "title": ID_UUID4_TITLE,
                "description": ID_UUID4_DESCRIPTION,
                "example": ID_UUID4_EXAMPLE,
                "examples": ID_UUID4_EXAMPLES,
            }
        case _:
            params = {}
    return params


def _add_description_prefix(params: dict[str, Any], prefix: str) -> None:
    if prefix != "":
        params["description"] = prefix + params.get("description", "")


def IDPath(  # noqa: N802
    _type: IDTypesEnum = IDTypesEnum.bson,
    alias: str = ID_DEFAULT_ALIAS,
    description_prefix: str = "",
) -> Any:
    params = _dispatch_params(_type)
    _add_description_prefix(params, description_prefix)
    return Path(**params, alias=alias)


def IDField(  # noqa: N802
    _type: IDTypesEnum = IDTypesEnum.bson,
    alias: str = ID_DEFAULT_ALIAS,
    description_prefix: str = "",
) -> Any:
    params = _dispatch_params(_type)
    _add_description_prefix(params, description_prefix)
    return Field(**params, alias=alias)


def IDQuery(  # noqa: N802
    _type: IDTypesEnum = IDTypesEnum.bson,
    alias: str = ID_DEFAULT_ALIAS,
    description_prefix: str = "",
) -> Any:
    params = _dispatch_params(_type)
    _add_description_prefix(params, description_prefix)
    return Query(**params, alias=alias)
