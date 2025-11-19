import asyncio
from collections.abc import Iterable
from copy import copy
from typing import TYPE_CHECKING, Any

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
    ReturnModel: "BaseModel",
    ProjectionModel: "BaseModel",
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

    count_query = count_query.find(
        session=session,
        ignore_cache=ctx.ignore_cache,
        **ctx.pymongo_kwargs,
    )

    find_query = find_query.find_many(
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
    )

    total, items = await _execute_queries(
        count_query=count_query,
        find_query=find_query,
        items_return_type=items_return_type,
        projection_model=projection_model,
    )

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
    ReturnModel: "BaseModel",
    ProjectionModel: "BaseModel",
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

    count_query = count_query.find(
        session=session,
        ignore_cache=ctx.ignore_cache,
        **ctx.pymongo_kwargs,
    )

    find_query = find_query.find_many(
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
    )

    total, items = await _execute_queries(
        count_query=count_query,
        find_query=find_query,
        items_return_type=items_return_type,
        projection_model=projection_model,
    )

    return LimitOffsetPageDTO(
        items=items,
        total=total,
        limit=params.limit,
        offset=params.offset,
    )


async def paginator_cursor[  # noqa: PLR0913
    DocType: Document,
    ReturnModel: "BaseModel",
    ProjectionModel: "BaseModel",
](
    query: _FindManyQueryType[DocType, ProjectionModel],
    params: "PaginationCursorParamsProtocol",
    session: "AsyncClientSession",
    items_return_type: _ReturnModelType[ReturnModel],
    ctx: QueryContext = QueryContext(),
    # TODO: Добавить сортировку с питом Sort
    # sort: Sort = None,
    sort: str | None = None,
    projection_model: _ProjectionModelType[ProjectionModel] = None,
) -> _CursorReturnType[ReturnModel]:
    if items_return_type is None:
        msg = "Either items_return_type must be provided"
        raise ValueError(msg)

    is_prev_cursor = _is_previous_cursor(params.cursor)

    count_query = copy(query)
    records_query = copy(query)
    find_query = copy(query)

    conditions = {}

    if sort is None:
        conditions = _condition_by_id(params.cursor)
        sort = SORT_DESC_PREFIX + KeysEnum.id if is_prev_cursor else sort
    elif params.cursor is not None:
        sort, field, key = _separate_sort(sort, is_prev_cursor)

        records = await records_query.find(
            {KeysEnum.id: convert_to_id(params.cursor)},
            session=session,
            ignore_cache=ctx.ignore_cache,
            **ctx.pymongo_kwargs,
        ).to_list()

        conditions = {field: {key: getattr(records[0], field)}}

    count_query = count_query.find(
        {},
        session=session,
        ignore_cache=ctx.ignore_cache,
        **ctx.pymongo_kwargs,
    )

    find_query = find_query.find_many(
        limit=params.size + 1,
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
    find_query = find_query.find(
        conditions,
        session=session,
        projection_model=projection_model,
        ignore_cache=ctx.ignore_cache,
        fetch_links=ctx.fetch_links,
        nesting_depth=ctx.nesting_depth,
        nesting_depths_per_field=ctx.nesting_depths_per_field,
        lazy_parse=ctx.lazy_parse,
        **ctx.pymongo_kwargs,
    )

    total, items = await _execute_queries(
        count_query=count_query,
        find_query=find_query,
        items_return_type=items_return_type,
        projection_model=projection_model,
    )

    is_have_next = len(items) > params.size

    items = _reverse_docs(is_prev_cursor, items[: params.size])

    if not hasattr(items[0], "id") or not hasattr(items[-1], "id"):
        msg = "The items return model must have an id attribute"
        raise AttributeError(msg)

    next_page = str(items[-1].id) if is_have_next else None
    previous_page = f"{CURSOR_PREVIOUS_PREFIX}{items[0].id}"

    return CursorPageDTO(
        items=items,
        total=total,
        current_page=params.cursor,
        previous_page=previous_page,
        next_page=next_page,
    )


async def _execute_queries[
    DocType: Document,
    ReturnModel: "BaseModel",
    ProjectionModel: "BaseModel",
](
    *,
    count_query: _FindManyQueryType[DocType, ProjectionModel],
    find_query: _FindManyQueryType[DocType, ProjectionModel],
    items_return_type: _ReturnModelType[ReturnModel],
    projection_model: _ProjectionModelType[ProjectionModel] = None,
) -> tuple[int, list[ReturnModel]]:
    total, documents = await asyncio.gather(
        count_query.count(),
        find_query.to_list(),
    )

    if not documents:
        raise NoContentError

    if not isinstance(documents, Iterable):
        msg = "The find query documents result must be iterable"
        raise TypeError(msg)

    if projection_model is not None:
        items = [
            items_return_type(**document.model_dump()) for document in documents
        ]
    else:
        items = convert_to_dtos(
            documents, items_return_type, is_replace_links=True
        )

    return total, items


def _reverse_docs[ReturnModel: "BaseModel"](
    is_prev_cursor: bool, documents: list[ReturnModel]
) -> list[ReturnModel]:
    return list(reversed(documents)) if is_prev_cursor else documents


def _separate_sort(
    sort: str, is_prev_cursor: bool
) -> tuple[str, str, KeysEnum]:
    if sort.startswith(SORT_DESC_PREFIX):
        return (
            sort.removeprefix(SORT_DESC_PREFIX) if is_prev_cursor else sort,
            sort.removeprefix(SORT_DESC_PREFIX),
            KeysEnum.gt if is_prev_cursor else KeysEnum.lt,
        )
    return (
        SORT_DESC_PREFIX + sort if is_prev_cursor else sort,
        sort,
        KeysEnum.lt if is_prev_cursor else KeysEnum.gt,
    )


def _condition_by_id(cursor: str | None) -> dict[KeysEnum | str, Any]:
    if cursor:
        if _is_previous_cursor(cursor):
            return {KeysEnum.id: {KeysEnum.lt: convert_to_id(cursor)}}
        return {KeysEnum.id: {KeysEnum.gt: convert_to_id(cursor)}}
    return {}


def _is_previous_cursor(cursor_string: str | None) -> bool:
    return (
        cursor_string.startswith(CURSOR_PREVIOUS_PREFIX)
        if cursor_string
        else False
    )
