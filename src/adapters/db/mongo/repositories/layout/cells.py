import asyncio
from typing import TYPE_CHECKING

from common.core.decorators import transaction
from common.core.exceptions import NoContentError
from common.core.hashing import get_md5hash
from common.mongo import (
    AddMixin,
    DecRefCountMixin,
    DeleteWithRefCountMixin,
    GetByHashMixin,
    GetByIDsMixin,
    GetMixin,
    IncRefCountMixin,
    UpdateMixin,
)

from src.application.dtos.db import (
    LayoutSchemaCreateDTO,
    LayoutSchemaDB,
    LayoutSchemaUpdateDTO,
    LayoutStyleCreateDTO,
    LayoutStyleDB,
    LayoutStyleUpdateDTO,
    LayoutValidationCreateDTO,
    LayoutValidationDB,
    LayoutValidationUpdateDTO,
)

if TYPE_CHECKING:
    from pydantic import BaseModel
    from pymongo.asynchronous.client_session import AsyncClientSession


class _Repository[
    ReturnSchema: BaseModel,
    CreateSchema: BaseModel,
    UpdateSchema: BaseModel,
](
    GetMixin[ReturnSchema],
    GetByIDsMixin[ReturnSchema],
    GetByHashMixin[ReturnSchema],
    AddMixin[CreateSchema, ReturnSchema],
    UpdateMixin[UpdateSchema, ReturnSchema],
    DeleteWithRefCountMixin,
    DecRefCountMixin,
    IncRefCountMixin,
):
    async def add(
        self,
        condition: CreateSchema,
        *,
        session: "AsyncClientSession",
    ) -> ReturnSchema:
        if not hasattr(condition, "hash"):
            msg = "'hash' field is required in condition"
            raise AssertionError(msg)

        condition.hash = get_md5hash(
            condition.model_dump(exclude={"hash", "id", "ref_count"})
        )
        try:
            return await self.get_by_hash(condition.hash, session=session)
        except NoContentError:
            return await super().add(condition, session=session)

    @transaction
    async def update(
        self,
        _id: str,
        condition: UpdateSchema,
        *,
        session: "AsyncClientSession",
    ) -> ReturnSchema:
        if not hasattr(condition, "hash"):
            msg = "'hash' field is required in condition"
            raise AssertionError(msg)

        obj = await self.get(_id, session=session)

        if not hasattr(obj, "ref_count"):
            msg = "'ref_count' field is required in db document"
            raise AssertionError(msg)

        for field in condition.model_fields_set:
            if field in obj.model_fields_set:
                setattr(obj, field, getattr(condition, field))

        condition.hash = get_md5hash(
            obj.model_dump(exclude={"hash", "id", "ref_count"})
        )

        try:
            document = await self.get_by_hash(condition.hash, session=session)

            if not hasattr(document, "id"):
                msg = "'id' field is required in db document"
                raise AssertionError(msg)

            async with asyncio.TaskGroup() as tg:
                tg.create_task(self.inc_ref(document.id, session=session))
                if obj.ref_count <= 0:
                    tg.create_task(self.delete(_id, session=session))
                else:
                    tg.create_task(self.dec_ref(_id, session=session))
        except NoContentError:
            return await super().update(_id, condition, session=session)
        else:
            return document


class LayoutSchemaRepository(
    _Repository[
        LayoutSchemaDB,
        LayoutSchemaCreateDTO,
        LayoutSchemaUpdateDTO,
    ]
):
    pass


class LayoutStyleRepository(
    _Repository[
        LayoutStyleDB,
        LayoutStyleCreateDTO,
        LayoutStyleUpdateDTO,
    ]
):
    pass


class LayoutValidationRepository(
    _Repository[
        LayoutValidationDB,
        LayoutValidationCreateDTO,
        LayoutValidationUpdateDTO,
    ]
):
    pass
