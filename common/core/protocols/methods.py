from typing import Protocol

from pydantic import BaseModel

from .session import SessionProtocol


class GetterProtocol[
    ReturnSchema: BaseModel,
    Session: SessionProtocol,
](Protocol):
    async def get(
        self, _id: str, *, session: Session | None = None
    ) -> ReturnSchema: ...


class AdderProtocol[
    CreateSchema: BaseModel,
    ReturnSchema: BaseModel,
    Session: SessionProtocol,
](Protocol):
    async def add(
        self, condition: CreateSchema, *, session: Session | None = None
    ) -> ReturnSchema: ...


class UpdaterProtocol[
    UpdateSchema: BaseModel,
    ReturnSchema: BaseModel,
    Session: SessionProtocol,
](Protocol):
    async def update(
        self,
        _id: str,
        condition: UpdateSchema,
        *,
        session: Session | None = None,
    ) -> ReturnSchema: ...


class DeleterProtocol[Session: SessionProtocol](Protocol):
    async def delete(
        self, _id: str, *, session: Session | None = None
    ) -> str: ...


class ExistedProtocol[Session: SessionProtocol](Protocol):
    async def exists(
        self, _id: str, *, session: Session | None = None
    ) -> bool: ...


class CountProtocol[Session: SessionProtocol](Protocol):
    async def count(self, *, session: Session | None = None) -> int: ...


class BulkAdd[
    CreateSchema: BaseModel,
    ReturnSchema: BaseModel,
    Session: SessionProtocol,
](Protocol):
    async def bulk_add(
        self, conditions: list[CreateSchema], *, session: Session | None = None
    ) -> list[ReturnSchema]: ...


class BulkAddWithReturnId[
    CreateSchema: BaseModel,
    Session: SessionProtocol,
](Protocol):
    async def bulk_add_with_return_id(
        self, conditions: list[CreateSchema], *, session: Session | None = None
    ) -> list[str]: ...


class BulkUpdate[
    UpdateSchema: BaseModel,
    ReturnSchema: BaseModel,
    Session: SessionProtocol,
](Protocol):
    async def bulk_update(
        self, conditions: list[UpdateSchema], *, session: Session | None = None
    ) -> list[ReturnSchema]: ...


class BulkUpdateWithReturnId[
    UpdateSchema: BaseModel,
    Session: SessionProtocol,
](Protocol):
    async def bulk_update_with_return_id(
        self, conditions: list[UpdateSchema], *, session: Session | None = None
    ) -> list[str]: ...
