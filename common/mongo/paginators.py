from collections.abc import Iterable
from copy import copy
from typing import TYPE_CHECKING

from common.core.constants import CURSOR_PREVIOUS_PREFIX, SORT_DESC_PREFIX
from common.core.dtos.pagination import (
    CursorPageDTO,
    LimitOffsetPageDTO,
    PagesPageDTO,
)
from common.core.exceptions import NoContentError

from .custom_types import Sort
from .enums import KeysEnum
from .utils import QueryContext, convert_to_dtos, convert_to_id

if TYPE_CHECKING:
    from beanie import Document
    from beanie.odm.queries.find import FindMany
    from pydantic import BaseModel
    from pymongo.asynchronous.client_session import AsyncClientSession

    from common.core.protocols import (
        PaginationCursorParamsProtocol,
        PaginationLimitOffsetParamsProtocol,
        PaginationPagesParamsProtocol,
    )


type _FindManyQueryType[DocType, ProjectionModelType] = (
    FindMany[DocType] | FindMany[ProjectionModelType]
)
type _CountQueryType[DocType] = FindMany[DocType]
type _ReturnModelType[ReturnModel: BaseModel] = type[ReturnModel]
type _ProjectionModelType[ProjectionModel] = type[ProjectionModel] | None
type _LimitOffsetReturnType[ReturnModel] = LimitOffsetPageDTO[ReturnModel]
type _PagesReturnType[ReturnModel] = PagesPageDTO[ReturnModel]
type _CursorReturnType[ReturnModel] = CursorPageDTO[ReturnModel]
type _ReturnItemsType[ReturnModel, ProjectionModel] = (
    ReturnModel | ProjectionModel
)

# TODO: Добавить ошибки по некорректно заданным параметрам пагинации


async def paginator_pages[  # noqa: PLR0913
    DocType: Document,
    ReturnModel: BaseModel,
    ProjectionModel: BaseModel,
](
    query: _FindManyQueryType[DocType, ProjectionModel],
    params: "PaginationPagesParamsProtocol",
    session: "AsyncClientSession",
    items_return_type: _ReturnModelType[ReturnModel],
    ctx: QueryContext = QueryContext(),
    sort: Sort = None,
    projection_model: _ProjectionModelType[ProjectionModel] = None,
) -> _PagesReturnType[ReturnModel]:
    if items_return_type is None:
        msg = "Either items_return_type must be provided"
        raise ValueError(msg)

    skip = (params.number - 1) * params.size
    limit = params.size

    count_query = copy(query)
    find_query = copy(query)

    total = await count_query.find(
        session=session,
        ignore_cache=ctx.ignore_cache,
        fetch_links=ctx.fetch_links,
        **ctx.pymongo_kwargs,
    ).count()

    documents = await find_query.find_many(
        limit=limit,
        skip=skip,
        session=session,
        projection_model=projection_model,
        sort=sort,
        ignore_cache=ctx.ignore_cache,
        fetch_links=ctx.fetch_links,
        nesting_depth=ctx.nesting_depth,
        nesting_depths_per_field=ctx.nesting_depths_per_field,
        lazy_parse=ctx.lazy_parse,
        **ctx.pymongo_kwargs,
    ).to_list()

    if not documents:
        raise NoContentError

    items = convert_items(documents, items_return_type, projection_model)  # type: ignore

    total_pages = total // params.size
    if params.size * total_pages < total:
        total_pages += 1
    next_page = (
        params.number + 1
        if total_pages > 1 and params.number < total_pages
        else None
    )
    previous_page = (
        params.number - 1 if total_pages > 1 and params.number > 1 else None
    )

    return PagesPageDTO(
        items=items,
        total=total_pages,
        current_page=params.number,
        previous_page=previous_page,
        next_page=next_page,
    )


async def paginator_limit_offset[  # noqa: PLR0913
    DocType: Document,
    ReturnModel: BaseModel,
    ProjectionModel: BaseModel,
](
    query: _FindManyQueryType[DocType, ProjectionModel],
    params: "PaginationLimitOffsetParamsProtocol",
    session: "AsyncClientSession",
    items_return_type: _ReturnModelType[ReturnModel],
    ctx: QueryContext = QueryContext(),
    sort: Sort = None,
    projection_model: _ProjectionModelType[ProjectionModel] = None,
) -> _LimitOffsetReturnType[ReturnModel]:
    if items_return_type is None:
        msg = "Either items_return_type must be provided"
        raise ValueError(msg)

    count_query = copy(query)
    find_query = copy(query)

    total = await count_query.find(
        session=session,
        ignore_cache=ctx.ignore_cache,
        fetch_links=ctx.fetch_links,
        **ctx.pymongo_kwargs,
    ).count()

    documents = await find_query.find_many(
        limit=params.limit,
        skip=params.offset,
        session=session,
        projection_model=projection_model,
        sort=sort,
        ignore_cache=ctx.ignore_cache,
        fetch_links=ctx.fetch_links,
        nesting_depth=ctx.nesting_depth,
        nesting_depths_per_field=ctx.nesting_depths_per_field,
        lazy_parse=ctx.lazy_parse,
        **ctx.pymongo_kwargs,
    ).to_list()

    if not documents:
        raise NoContentError

    items = convert_items(documents, items_return_type, projection_model)  # type: ignore

    return LimitOffsetPageDTO(
        items=items,
        total=total,
        limit=params.limit,
        offset=params.offset,
    )


async def paginator_cursor[  # noqa: PLR0913
    DocType: Document,
    ReturnModel: BaseModel,
    ProjectionModel: BaseModel,
](
    query: _FindManyQueryType[DocType, ProjectionModel],
    params: "PaginationCursorParamsProtocol",
    session: "AsyncClientSession",
    items_return_type: _ReturnModelType[ReturnModel],
    ctx: QueryContext = QueryContext(),
    sort: Sort = None,
    projection_model: _ProjectionModelType[ProjectionModel] = None,
) -> _CursorReturnType[ReturnModel]:
    if items_return_type is None:
        msg = "Either items_return_type must be provided"
        raise ValueError(msg)

    count_query = copy(query)
    find_query = copy(query)

    total = await count_query.find(
        session=session,
        ignore_cache=ctx.ignore_cache,
        fetch_links=ctx.fetch_links,
        **ctx.pymongo_kwargs,
    ).count()

    find_query = find_query.find_many(
        session=session,
        projection_model=projection_model,
        sort=sort,
        ignore_cache=ctx.ignore_cache,
        fetch_links=ctx.fetch_links,
        nesting_depth=ctx.nesting_depth,
        nesting_depths_per_field=ctx.nesting_depths_per_field,
        lazy_parse=ctx.lazy_parse,
        **ctx.pymongo_kwargs,
    )

    if params.cursor:
        if _is_previous_cursor(params.cursor):
            find_query = find_query.find(
                {KeysEnum.id: {KeysEnum.gt: convert_to_id(params.cursor)}},
            ).sort(SORT_DESC_PREFIX + KeysEnum.id)
        else:
            find_query = find_query.find(
                {KeysEnum.id: {KeysEnum.lt: convert_to_id(params.cursor)}}
            )

    documents = await find_query.limit(params.size + 1).to_list()

    if not documents:
        raise NoContentError

    items = convert_items(documents, items_return_type, projection_model)  # type: ignore

    if _is_previous_cursor(params.cursor):
        items = list(reversed(items[: params.size]))

    if not hasattr(items[0], "id") or not hasattr(items[-1], "id"):
        msg = "The items return model must have an id attribute"
        raise AttributeError(msg)

    next_page = str(items[-1].id) if len(items) > params.size else None
    previous_page = f"{CURSOR_PREVIOUS_PREFIX}{items[0].id}"

    return CursorPageDTO(
        items=items,
        total=total,
        current_page=params.cursor,
        previous_page=previous_page,
        next_page=next_page,
    )


def convert_items[
    DocType: Document,
    ReturnModel: BaseModel,
    ProjectionModel: BaseModel,
](
    documents: Iterable[DocType],
    return_model: _ReturnModelType[ReturnModel],
    projection_model: _ProjectionModelType[ProjectionModel] = None,
) -> list[ReturnModel]:
    if projection_model is not None:
        items = [return_model(**d.model_dump()) for d in documents]
    else:
        items = convert_to_dtos(documents, return_model, is_replace_links=True)
    return items


def _is_previous_cursor(cursor_string: str | None) -> bool:
    return (
        cursor_string.startswith(CURSOR_PREVIOUS_PREFIX)
        if cursor_string
        else False
    )
