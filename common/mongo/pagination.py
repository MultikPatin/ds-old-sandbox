# import asyncio
# from copy import copy, deepcopy
# from typing import TYPE_CHECKING, Any
#
# from beanie.odm.queries.aggregation import AggregationQuery
#
# from common.core.constants import CURSOR_PREVIOUS_PREFIX, SORT_DESC_PREFIX
# from common.core.dtos.pagination import (
#     CursorPageDTO,
#     LimitOffsetPageDTO,
#     PagesPageDTO,
# )
# from common.core.exceptions import NoContentError
#
# from .enums import KeysEnum
# from .utils import convert_to_dtos, convert_to_id
#
# if TYPE_CHECKING:
#     from beanie import Document
#     from beanie.odm.enums import SortDirection
#     from beanie.odm.queries.find import FindMany
#     from pydantic import BaseModel
#     from pymongo.asynchronous.client_session import AsyncClientSession
#
#     from common.core.protocols import (
#         PaginationCursorParamsProtocol,
#         PaginationLimitOffsetParamsProtocol,
#         PaginationPagesParamsProtocol,
#     )
#
# type Query[DocType] = DocType | FindMany[DocType] | AggregationQuery[DocType]
# type Sort = None | str | list[tuple[str, SortDirection]]
#
#
# async def paginator_limit_offset[DocType: Document,
# PydanticModel: "BaseModel"](
#     query: Query[DocType],
#     params: "PaginationLimitOffsetParamsProtocol",
#     items_return_type: type[PydanticModel],
#     session: "AsyncClientSession",
#     sort: Sort = None,
#     ignore_cache: bool = False,
#     fetch_links: bool = False,
#     nesting_depth: int | None = None,
#     nesting_depths_per_field: dict[str, int] | None = None,
#     lazy_parse: bool = False,
#     **pymongo_kwargs: Any,
# ) -> LimitOffsetPageDTO[PydanticModel]:
#     if isinstance(query, AggregationQuery):
#         total, documents = await _find_documents(
#             data=[
#                 {KeysEnum.limit: params.limit + (params.offset or 0)},
#                 {KeysEnum.skip: params.offset},
#             ],
#             query=deepcopy(query),
#         )
#     else:
#         count_query = copy(query)
#         find_query = copy(query)
#
#         count_query = count_query.find(
#             session=session,
#             ignore_cache=ignore_cache,
#             **pymongo_kwargs,
#         )
#
#         find_query = find_query.find_many(
#             limit=params.limit,
#             skip=params.offset,
#             session=session,
#             sort=sort,
#             ignore_cache=ignore_cache,
#             fetch_links=fetch_links,
#             nesting_depth=nesting_depth,
#             nesting_depths_per_field=nesting_depths_per_field,
#             lazy_parse=lazy_parse,
#             **pymongo_kwargs,
#         )
#
#         total, documents = await _execute_queries(count_query, find_query)
#
#     if not documents:
#         raise NoContentError
#
#     return LimitOffsetPageDTO(
#         items=convert_to_dtos(documents, items_return_type,
#         replace_links=True),
#         total=total,
#         limit=params.limit,
#         offset=params.offset,
#     )
#
#
# async def paginator_pages[DocType: Document, PydanticModel: "BaseModel"](
#     query: Query[DocType],
#     params: "PaginationPagesParamsProtocol",
#     items_return_type: type[PydanticModel],
#     session: "AsyncClientSession",
#     sort: Sort = None,
#     ignore_cache: bool = False,
#     fetch_links: bool = False,
#     nesting_depth: int | None = None,
#     nesting_depths_per_field: dict[str, int] | None = None,
#     lazy_parse: bool = False,
#     **pymongo_kwargs: Any,
# ) -> PagesPageDTO[PydanticModel]:
#     skip = (params.number - 1) * params.size
#     limit = params.size
#
#     if isinstance(query, AggregationQuery):
#         total, documents = await _find_documents(
#             data=[
#                 {KeysEnum.limit: limit},
#                 {KeysEnum.skip: skip},
#             ],
#             query=deepcopy(query),
#         )
#     else:
#         count_query = copy(query)
#         find_query = copy(query)
#
#         count_query = count_query.find(
#             {},
#             session=session,
#             ignore_cache=ignore_cache,
#             **pymongo_kwargs,
#         )
#
#         find_query = find_query.find_many(
#             limit=limit,
#             skip=skip,
#             session=session,
#             sort=sort,
#             ignore_cache=ignore_cache,
#             fetch_links=fetch_links,
#             nesting_depth=nesting_depth,
#             nesting_depths_per_field=nesting_depths_per_field,
#             lazy_parse=lazy_parse,
#             **pymongo_kwargs,
#         )
#
#         total, documents = await _execute_queries(count_query, find_query)
#
#     if not documents:
#         raise NoContentError
#
#     total_pages = total // params.size
#     if params.size * total_pages < total:
#         total_pages += 1
#     next_page = (
#         params.number + 1
#         if total_pages > 1 and params.number < total_pages
#         else None
#     )
#     previous_page = (
#         params.number - 1 if total_pages > 1 and params.number > 1 else None
#     )
#
#     return PagesPageDTO(
#         items=convert_to_dtos(documents, items_return_type,
#         replace_links=True),
#         total=total_pages,
#         current_page=params.number,
#         previous_page=previous_page,
#         next_page=next_page,
#     )
#
#
# async def paginator_cursor[DocType: Document, PydanticModel: "BaseModel"](
#     query: Query[DocType],
#     params: "PaginationCursorParamsProtocol",
#     items_return_type: type[PydanticModel],
#     session: "AsyncClientSession",
#     sort: str | None = None,
#     ignore_cache: bool = False,
#     fetch_links: bool = False,
#     nesting_depth: int | None = None,
#     nesting_depths_per_field: dict[str, int] | None = None,
#     lazy_parse: bool = False,
#     **pymongo_kwargs: Any,
# ) -> CursorPageDTO[PydanticModel]:
#     is_prev_cursor = _is_previous_cursor(params.cursor)
#
#     if isinstance(query, AggregationQuery):
#         agg_query = deepcopy(query)
#         if not sort:
#             total, documents = await _find_documents(
#                 data=_cursor_data(params),
#                 query=agg_query,
#             )
#         else:
#             raise NotImplementedError
#     else:
#         count_query = copy(query)
#         records_query = copy(query)
#         find_query = copy(query)
#
#         conditions = {}
#
#         if sort is None:
#             conditions = _condition_by_id(params.cursor)
#             sort = SORT_DESC_PREFIX + KeysEnum.id if is_prev_cursor else sort
#         elif params.cursor is not None:
#             sort, field, key = _separate_sort(sort, is_prev_cursor)
#
#             records = await records_query.find(
#                 {KeysEnum.id: convert_to_id(params.cursor)},
#                 session=session,
#                 ignore_cache=ignore_cache,
#                 **pymongo_kwargs,
#             ).to_list()
#
#             conditions = {field: {key: getattr(records[0], field)}}
#
#         count_query = count_query.find(
#             {},
#             session=session,
#             ignore_cache=ignore_cache,
#             **pymongo_kwargs,
#         )
#
#         find_query = find_query.find_many(
#             limit=params.size + 1,
#             session=session,
#             sort=sort,
#             ignore_cache=ignore_cache,
#             fetch_links=fetch_links,
#             nesting_depth=nesting_depth,
#             nesting_depths_per_field=nesting_depths_per_field,
#             lazy_parse=lazy_parse,
#             **pymongo_kwargs,
#         )
#         find_query = find_query.find(
#             conditions,
#             session=session,
#             ignore_cache=ignore_cache,
#             fetch_links=fetch_links,
#             nesting_depth=nesting_depth,
#             nesting_depths_per_field=nesting_depths_per_field,
#             lazy_parse=lazy_parse,
#             **pymongo_kwargs,
#         )
#
#         total, documents = await _execute_queries(count_query, find_query)
#
#     if not documents:
#         raise NoContentError
#
#     is_have_next = len(documents) > params.size
#
#     documents = _reverse_docs(is_prev_cursor, documents[: params.size])
#
#     next_page = str(documents[-1].id) if is_have_next else None
#     previous_page = f"{CURSOR_PREVIOUS_PREFIX}{documents[0].id}"
#
#     return CursorPageDTO(
#         items=convert_to_dtos(documents, items_return_type,
#         replace_links=True),
#         total=total,
#         current_page=params.cursor,
#         previous_page=previous_page,
#         next_page=next_page,
#     )
#
#
# async def _execute_queries[DocType: Document](
#     count_query: "FindMany[DocType]",
#     find_query: "FindMany[DocType]",
# ) -> tuple[int, list[DocType]]:
#     return await asyncio.gather(
#         count_query.count(),
#         find_query.to_list(),
#     )
#
#
# def _reverse_docs[DocType: Document](
#     is_prev_cursor: bool, documents: list[DocType]
# ) -> list[DocType]:
#     return list(reversed(documents)) if is_prev_cursor else documents
#
#
# def _is_previous_cursor(cursor_string: str | None) -> bool:
#     return (
#         cursor_string.startswith(CURSOR_PREVIOUS_PREFIX)
#         if cursor_string
#         else False
#     )
#
#
# def _separate_sort(
#     sort: str, is_prev_cursor: bool
# ) -> tuple[str, str, KeysEnum]:
#     if sort.startswith(SORT_DESC_PREFIX):
#         return (
#             sort.removeprefix(SORT_DESC_PREFIX) if is_prev_cursor else sort,
#             sort.removeprefix(SORT_DESC_PREFIX),
#             KeysEnum.gt if is_prev_cursor else KeysEnum.lt,
#         )
#     return (
#         SORT_DESC_PREFIX + sort if is_prev_cursor else sort,
#         sort,
#         KeysEnum.lt if is_prev_cursor else KeysEnum.gt,
#     )
#
#
# def _condition_by_id(cursor: str | None) -> dict[KeysEnum | str, Any]:
#     if cursor:
#         if _is_previous_cursor(cursor):
#             return {KeysEnum.id: {KeysEnum.lt: convert_to_id(cursor)}}
#         return {KeysEnum.id: {KeysEnum.gt: convert_to_id(cursor)}}
#     return {}
#
#
# def _cursor_data(
#     params: "PaginationCursorParamsProtocol",
# ) -> list[dict[KeysEnum | str, Any]]:
#     if params.cursor:
#         return [
#             {KeysEnum.limit: params.size + 1},
#             _condition_by_id(params.cursor),
#         ]
#     return []
#
#
# async def _find_documents[DocType: Document](
#     data: list[dict[KeysEnum | str, Any]],
#     query: AggregationQuery[DocType],
# ) -> tuple[int, list[DocType] | None]:
#     query.aggregation_pipeline.extend(
#         [
#             {
#                 KeysEnum.facet: {
#                     "metadata": [{KeysEnum.count: "total"}],
#                     "data": data,
#                 }
#             },
#         ],
#     )
#     data = (await query.to_list())[0]
#     documents = data["data"]
#
#     try:
#         total = data["metadata"][0]["total"]
#     except IndexError:
#         total = 0
#
#     return total, documents
