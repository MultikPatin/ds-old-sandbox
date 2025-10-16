from datetime import UTC, datetime

from common.core.enums import LifeStatusEnum
from common.core.exceptions import NoContentError
from common.mongo import (
    AddMixin,
    KeysEnum,
    convert_to_dto,
    convert_to_id,
)
from pymongo.asynchronous.client_session import AsyncClientSession

from src.adapters.db.mongo.documents import InputsDocument
from src.application.dtos.db.input import (
    InputDB,
    InputFullLinks,
    InputLayoutIDProject,
    InputUpdateDTO,
)
from src.application.dtos.input import InputCreate

from .block import rebuild_singles, rebuild_tables


class InputRepository(AddMixin[InputCreate, InputDB]):
    async def get_full_links(
        self, _id: str, *, session: AsyncClientSession | None = None
    ) -> InputFullLinks:
        document = await self._get_with_links(_id, session=session)
        return convert_to_dto(document, InputFullLinks)

    async def update_full_links(
        self,
        _id: str,
        condition: InputUpdateDTO,
        *,
        session: AsyncClientSession | None = None,
    ) -> InputFullLinks:
        # TODO: Вынести глубину вложенности в отдельный конфиг возможно?
        specific_nesting_field = {"singles": 0, "tables": 0}
        if condition.singles is not None:
            specific_nesting_field["singles"] = 1
        if condition.tables is not None:
            specific_nesting_field["tables"] = 2

        document = await self._get_with_links(
            _id,
            session=session,
            specific_nesting_field=specific_nesting_field,
        )

        if document.singles is not None and condition.singles is not None:
            await rebuild_singles(
                document.singles, condition.singles, session=session
            )
        if document.tables is not None and condition.tables is not None:
            await rebuild_tables(
                document.tables, condition.tables, session=session
            )

        document.status = condition.status
        document.updated = condition.updated

        if condition.card is not None:
            document.card = condition.card

        if condition.options is not None:
            document.options = condition.options

        await document.save_changes(session=session)
        return convert_to_dto(document, InputFullLinks)

    async def get_layout_id(
        self, _id: str, *, session: AsyncClientSession | None = None
    ) -> str:
        document = await self._collection.find_one(
            {KeysEnum.id: convert_to_id(_id)},
            session=session,
            projection_model=InputLayoutIDProject,
            fetch_links=True,
            nesting_depths_per_field={"singles": 0, "tables": 0, "layout": 1},
        )
        if document is None:
            raise NoContentError
        return document.layout.id

    async def update_status(
        self,
        _id: str,
        status: LifeStatusEnum,
        *,
        session: AsyncClientSession | None = None,
    ) -> str:
        document = await self._get(_id, session=session)
        document.status = status
        document.updated = datetime.now(UTC)
        await document.save_changes(session=session)
        return _id

    async def delete(
        self, _id: str, *, session: AsyncClientSession | None = None
    ) -> str:
        document = await self._get(_id, session=session)
        document.status = LifeStatusEnum.deleted
        document.updated = datetime.now(UTC)
        await document.save_changes(session=session)
        return _id

    async def _get(
        self, _id: str, *, session: AsyncClientSession | None = None
    ) -> InputsDocument:
        document = await self._collection.find_one(
            {KeysEnum.id: convert_to_id(_id)},
            session=session,
        )
        if document is None:
            raise NoContentError
        return document

    async def _get_with_links(
        self,
        _id: str,
        *,
        session: AsyncClientSession | None = None,
        specific_nesting_field: dict[str, int] | None = None,
    ) -> InputsDocument:
        # TODO: Вынести глубину вложенности в отдельный конфиг возможно?
        nesting_depths_per_field = {"singles": 1, "tables": 2, "layout": 0}
        if specific_nesting_field is not None:
            for field, depth in specific_nesting_field.items():
                if field in nesting_depths_per_field:
                    nesting_depths_per_field[field] = depth

        document = await self._collection.find_one(
            {KeysEnum.id: convert_to_id(_id)},
            session=session,
            fetch_links=True,
            nesting_depths_per_field=nesting_depths_per_field,
        )
        if document is None:
            raise NoContentError
        return document
