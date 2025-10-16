from collections.abc import Iterable, MutableMapping, Sequence
from typing import Any

from beanie import BackLink, Document, Link, PydanticObjectId
from bson.errors import InvalidId
from pydantic import BaseModel

from common.core.constants import (
    CURSOR_SEPARATOR,
    ID_BSON_DESCRIPTION,
    ID_BSON_EXAMPLE,
    ID_BSON_TITLE,
)
from common.core.exceptions import (
    BusinessLogicError,
    BusinessLogicErrorContent,
)


def convert_to_id(_id: str) -> PydanticObjectId:
    s = _id.split(CURSOR_SEPARATOR, 1)

    try:
        if len(s) == 1:
            return PydanticObjectId(_id)
        return PydanticObjectId(s[-1])
    except InvalidId:
        raise BusinessLogicError(
            BusinessLogicErrorContent(
                message="Invalid id format",
                context={
                    "received_id": _id,
                    "required_fmt": {
                        "title": ID_BSON_TITLE,
                        "description": ID_BSON_DESCRIPTION,
                        "example": ID_BSON_EXAMPLE,
                    },
                },
            )
        )


def convert_to_dto[DocType: Document, PydanticModel: BaseModel](
    document: DocType,
    dto_class: type[PydanticModel],
    *,
    replace_links: bool = False,
) -> PydanticModel:
    document_data = document.model_dump()
    if replace_links:
        _replace_links(document_data)
    return dto_class.model_validate(document_data)


def convert_to_dtos[DocumentType: Document, PydanticModel: BaseModel](
    documents: Iterable[DocumentType],
    dto_class: type[PydanticModel],
    *,
    replace_links: bool = False,
) -> list[PydanticModel]:
    return [
        convert_to_dto(document, dto_class, replace_links=replace_links)
        for document in documents
    ]


def _replace_links(obj: MutableMapping[str, Any] | Sequence[Any]) -> None:
    if isinstance(obj, dict):
        to_delete = []
        for k in obj:
            if isinstance(obj[k], Link):
                obj[k] = str(obj[k].ref.id)
            elif isinstance(obj[k], BackLink):
                to_delete.append(k)
            else:
                _replace_links(obj[k])
        for k in to_delete:
            del obj[k]
    elif isinstance(obj, list):
        for item in obj:
            _replace_links(item)
