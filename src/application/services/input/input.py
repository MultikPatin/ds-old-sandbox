# from common.core.custom_types import AnyMatrix
# from common.core.decorators import transaction
# from common.core.enums import LifeStatusEnum
from typing import TYPE_CHECKING

from src.application.dtos import InputWithValuesDTO

from .replacer import get_chunk_ids, replace_layers

# from src.application.dtos.db.input import (
# InputTableChunkDB,
# InputTableFullLinks,
# InputTableInMatrix,
# InputUpdateDTO,
# InputCreateDTO,
# )

# from src.application.dtos.input import InputCreate


# from .card import generate_card

if TYPE_CHECKING:
    from common.core.protocols import SessionProtocol

    from src.application.dtos.db import InputDB, InputFullLinks
    from src.application.protocols import (
        InputRepositoryProtocol,
        # InputCardServiceProtocol,
        # InputSingleServiceProtocol,
        InputTableChunkServiceProtocol,
        # InputTableServiceProtocol,
        InputToolsServiceProtocol,
    )


class InputService:
    def __init__(
        self,
        repo: "InputRepositoryProtocol[SessionProtocol]",
        *,
        # card_service: "InputCardServiceProtocol",
        # single_service: "InputSingleServiceProtocol",
        # table_service: "InputTableServiceProtocol",
        table_chunk_service: "InputTableChunkServiceProtocol",
        tools_service: "InputToolsServiceProtocol",
    ):
        self._repo = repo
        # self._card = card_service
        # self._single = single_service
        # self._table = table_service
        self._chunk = table_chunk_service
        self._tool = tools_service

    async def add_as_template(
        self, layout_key: str, *, session: "SessionProtocol"
    ) -> InputWithValuesDTO:
        template = await self._tool.template(layout_key, session=session)
        raise NotImplementedError

    async def delete_soft(self, _id: str, *, session: "SessionProtocol") -> str:
        return await self._repo.delete_soft(_id, session=session)

    async def get(self, _id: str, *, session: "SessionProtocol") -> "InputDB":
        return await self._repo.get(_id, session=session)

    async def get_full_links(
        self, _id: str, *, session: "SessionProtocol"
    ) -> "InputFullLinks":
        return await self._repo.get_full_links(_id, session=session)

    async def get_with_values(
        self, _id: str, *, session: "SessionProtocol"
    ) -> InputWithValuesDTO:
        instance = await self._repo.get_full_links(_id, session=session)
        ids = get_chunk_ids(instance)
        results = await self._chunk.get_by_ids(ids, session=session)
        changes = {r.id: r.model_dump() for r in results}
        # TODO Реализовать работу с отдачей чанка по номеру
        #   добавить фильтрацию к запросу
        #   добавить параметры в фильтр (chunk_number, total_chunks)
        #   первично или при пустых значениях отдавать первый чанк
        #   преобразование вести в методе _set_values
        return InputWithValuesDTO(**replace_layers(instance, changes))

    # @transaction
    # async def add(
    #     self,
    #     condition: InputCreateDTO,
    #     *,
    #     session: SessionProtocol | None = None,
    # ) -> InputWithTableInMatrix:
    #     # TODO Проработать вопрос работы с layout и валидацией
    #     # TODO Нужно вынести валидацию и generate_card из транзакции?
    #     card = await generate_card(condition.layout_id)
    #     single_ids = None
    #     tables_ids = None
    #     if condition.singles:
    #         single_ids = await self._single_service.bulk_add_with_return_id(
    #             condition.singles
    #         )
    #     if condition.tables:
    #         tables_ids = await self._table_service.bulk_add_with_return_id(
    #             condition.tables
    #         )
    #     instance = await self._repo.add(
    #         InputCreate(
    #             singles=single_ids,
    #             tables=tables_ids,
    #             layout=condition.layout_id,
    #             card=card,
    #         ),
    #         session=session,
    #     )
    #     # TODO Можно ли избавится от get?
    #     return await self.get(instance.id, session=session)
    #
    # async def update(
    #     self,
    #     _id: str,
    #     condition: InputUpdateDTO,
    #     *,
    #     session: SessionProtocol | None = None,
    # ) -> InputWithTableInMatrix:
    #     condition.layout_id = await self._repo.get_layout_id(
    #         _id, session=session
    #     )
    #     condition.card = await generate_card(condition.layout_id)
    #     # TODO Проработать вопрос работы с валидацией
    #     #   Детальная валидация при condition.status == LiveStatusEnum.published
    #     #   await self._validator.validate(condition)
    #     instance = await self._update(_id, condition, session=session)
    #     return await switch_tables_to_matrix(instance)
    #
    # @transaction
    # async def _update(
    #     self,
    #     _id: str,
    #     condition: InputUpdateDTO,
    #     *,
    #     session: SessionProtocol | None = None,
    # ) -> InputFullLinks:
    #     return await self._repo.update_full_links(
    #         _id, condition, session=session
    #     )
    #
    # async def update_status(
    #     self,
    #     _id: str,
    #     status: LifeStatusEnum,
    #     *,
    #     session: SessionProtocol | None = None,
    # ) -> LifeStatusEnum:
    #     instance_status = status
    #     if status == LifeStatusEnum.deleted:
    #         await self.delete(_id, session=session)
    #         instance_status = LifeStatusEnum.deleted
    #     elif status == LifeStatusEnum.published:
    #         # TODO Конкретизировать исключение
    #         #   запрет публикации через этот метод
    #         #   добавить данное исключение в responses
    #         msg = "Status cannot be changed to published in this endpoint"
    #         raise ValueError(msg)
    #     else:
    #         await self._repo.update_status(_id, status, session=session)
    #     return instance_status
    #


#
#
# async def matrix_from_chunks(
#     chunks: list[InputTableChunkDB], result: AnyMatrix
# ) -> None:
#     if chunks is not None:
#         for chunk in chunks:
#             result.extend(chunk.values)
#
#
# async def table_with_matrix(
#     table: InputTableFullLinks,
# ) -> InputTableInMatrix:
#     values: AnyMatrix = []
#     await matrix_from_chunks(table.chunks, values)
#     return InputTableInMatrix(
#         **table.model_dump(exclude={"chunks"}), values=values
#     )
#
#
# async def tables_with_matrix(
#     instance: InputFullLinks,
# ) -> list[InputTableInMatrix] | None:
#     return (
#         [await table_with_matrix(table) for table in instance.tables]
#         if instance.tables
#         else None
#     )
#
#
# async def switch_tables_to_matrix(
#     instance: InputFullLinks,
# ) -> InputWithTableInMatrix:
#     return InputWithTableInMatrix(
#         **instance.model_dump(exclude={"tables"}),
#         tables=await tables_with_matrix(instance),
#     )
