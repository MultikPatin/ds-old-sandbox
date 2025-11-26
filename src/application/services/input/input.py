import asyncio
from typing import TYPE_CHECKING

from common.core.decorators import transaction
from common.core.enums import LifeStatusEnum
from common.core.exceptions import BusinessLogicError, BusinessLogicErrorContent

from src.application.dtos import InputCreateValuesDTO, InputWithValuesDTO
from src.application.dtos.db import InputCreateDTO

if TYPE_CHECKING:
    from common.core.protocols import SessionProtocol

    from src.application.dtos.db import InputDB, InputWithBlocks
    from src.application.protocols import (
        InputRepositoryProtocol,
        # InputCardServiceProtocol,
        InputSingleServiceProtocol,
        InputTableServiceProtocol,
        InputToolsServiceProtocol,
    )


class InputService:
    def __init__(
        self,
        repo: "InputRepositoryProtocol[SessionProtocol]",
        *,
        # card_service: "InputCardServiceProtocol",
        single_service: "InputSingleServiceProtocol",
        table_service: "InputTableServiceProtocol",
        tools_service: "InputToolsServiceProtocol",
    ):
        self._repo = repo
        # self._card = card_service
        self._single = single_service
        self._table = table_service
        self._tool = tools_service

    async def delete_soft(self, _id: str, *, session: "SessionProtocol") -> str:
        return await self._repo.delete_soft(_id, session=session)

    async def get(self, _id: str, *, session: "SessionProtocol") -> "InputDB":
        return await self._repo.get(_id, session=session)

    async def get_full_links(
        self, _id: str, *, session: "SessionProtocol"
    ) -> "InputWithBlocks":
        return await self._repo.get_full_links(_id, session=session)

    async def get_with_values(
        self, _id: str, *, session: "SessionProtocol"
    ) -> InputWithValuesDTO:
        instance = await self._repo.get_full_links(_id, session=session)
        return await self._tool.set_table_values(instance, session=session)

    async def add_as_template(
        self, layout_key: str, *, session: "SessionProtocol"
    ) -> InputWithValuesDTO:
        template = await self._tool.template(layout_key, session=session)
        return await self._add(template, session=session)

    async def update_status(
        self, _id: str, status: LifeStatusEnum, *, session: "SessionProtocol"
    ) -> LifeStatusEnum:
        exclude = (
            LifeStatusEnum.deleted,  # Использовать delete method
            LifeStatusEnum.published,  # Использовать update method
        )
        if status in LifeStatusEnum.values(exclude):
            await self._repo.update_status(_id, status, session=session)
        else:
            raise BusinessLogicError(
                BusinessLogicErrorContent(
                    message="Attempt to change to an invalid status",
                    context={"invalid_statuses": [exclude]},
                )
            )
        return status

    @transaction
    async def _add(
        self,
        condition: InputCreateValuesDTO,
        *,
        session: "SessionProtocol",
    ) -> InputWithValuesDTO:
        s_tasks, t_tasks = None, None

        async with asyncio.TaskGroup() as tg:
            if condition.singles:
                s_tasks = tg.create_task(
                    self._single.bulk_add(condition.singles, session=session)
                )
            if condition.tables:
                t_tasks = tg.create_task(
                    self._table.bulk_add(condition.tables, session=session)
                )

        singles = s_tasks.result() if s_tasks else None
        tables = t_tasks.result() if t_tasks else None

        cond = InputCreateDTO(
            **condition.model_dump(exclude={"singles", "tables"}),
            singles=[s.id for s in singles] if singles else None,
            tables=[t.id for t in tables] if tables else None,
        )
        # TODO Продумать работу по генерации карточки
        instance = await self._repo.add(cond, session=session)
        # TODO При реализации отдачи чанков по номера
        #   предусмотреть отдачу только первого чанка
        return InputWithValuesDTO(
            **instance.model_dump(),
            singles=singles,
            tables=tables,
        )

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
    #     #   Детальная валидация при
    #     #   if condition.status == LiveStatusEnum.published
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
