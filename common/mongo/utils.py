from collections.abc import (
    Generator,
    Iterable,
    MutableMapping,
    Sequence,
    Set,
)
from typing import TYPE_CHECKING, Any

from abgroup_core.constants import (
    CURSOR_SEPARATOR,
    ID_BSON_DESCRIPTION,
    ID_BSON_EXAMPLE,
    ID_BSON_TITLE,
    SORT_DESC_PREFIX,
)
from abgroup_core.custom_types import AnyDict
from abgroup_core.exceptions import (
    BusinessLogicError,
    BusinessLogicErrorContent,
)
from beanie import BackLink, Link, PydanticObjectId
from beanie.odm.enums import SortDirection
from bson.errors import InvalidId
from pydantic import BaseModel, Field

from .custom_types import Sort

if TYPE_CHECKING:
    from beanie import Document


type ProjectionModelType[Model] = type[Model] | None


class QueryContext(BaseModel):
    ignore_cache: bool = False
    fetch_links: bool = False
    nesting_depth: int | None = None
    nesting_depths_per_field: dict[str, int] | None = None
    lazy_parse: bool = False
    pymongo_kwargs: AnyDict = Field(default_factory=dict)


def prepare_sort[Doctype: "Document"](
    sort: str | list[str] | None, document: type[Doctype]
) -> Sort:
    prepared_sort = _prepare_sort(sort)
    if not prepared_sort:
        return None
    result = [s for s in prepared_sort if hasattr(document, s[0])]
    if result:
        return result
    msg = f"Sorting by {sort} is not allowed"
    raise ValueError(msg)


def _prepare_sort(
    sort: str | list[str] | None,
) -> list[tuple[str, SortDirection]] | None:
    if sort is None:
        return None
    if isinstance(sort, str):
        return [_split_sort(sort)]
    return [_split_sort(s) for s in sort if isinstance(s, str)]


def _split_sort(sort: str) -> tuple[str, SortDirection]:
    if sort.startswith(SORT_DESC_PREFIX):
        return sort.removeprefix(SORT_DESC_PREFIX), SortDirection.DESCENDING
    return sort, SortDirection.ASCENDING


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
        ) from None


def convert_to_dto[DocType: "Document", PydanticModel: "BaseModel"](
    document: DocType,
    dto_class: type[PydanticModel],
    *,
    is_replace_links: bool = False,
) -> PydanticModel:
    document_data = document.model_dump()
    if is_replace_links:
        replace_links(document_data)
    return dto_class.model_validate(document_data)


def convert_to_dtos[DocType: "Document", PydanticModel: "BaseModel"](
    documents: Iterable[DocType],
    dto_class: type[PydanticModel],
    *,
    is_replace_links: bool = False,
) -> list[PydanticModel]:
    return [
        convert_to_dto(document, dto_class, is_replace_links=is_replace_links)
        for document in documents
    ]


def replace_links(obj: MutableMapping[str, Any] | Sequence[Any]) -> None:
    if isinstance(obj, dict):
        to_delete = []
        for k in obj:
            if isinstance(obj[k], Link):
                obj[k] = str(obj[k].ref.id)
            elif isinstance(obj[k], BackLink):
                to_delete.append(k)
            else:
                replace_links(obj[k])
        for k in to_delete:
            del obj[k]
    elif isinstance(obj, list):
        for item in obj:
            replace_links(item)


def generate_batches[Item: Any](
    data: Sequence[Item] | Set[Item], size: int | None = None
) -> Generator[Sequence[Item], None, None]:
    length = len(data)

    middle_length = 100
    max_length = 1000

    if size is None:
        if length <= middle_length:
            s = 10
        elif length <= max_length:
            s = 50
        else:
            s = middle_length
    else:
        s = min(size, max_length)

    if isinstance(data, Set):
        data = list(data)

    return (data[i : i + s] for i in range(0, length, s))
