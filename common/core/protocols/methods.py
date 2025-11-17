from collections.abc import Sequence, Set
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from pydantic import BaseModel

    from .session import SessionProtocol


class GetterProtocol[
    ReturnSchema: "BaseModel",
    Session: "SessionProtocol",
](Protocol):
    async def get(self, _id: str, *, session: Session) -> ReturnSchema: ...


class GetterByIDsProtocol[
    ReturnSchema: "BaseModel",
    Session: "SessionProtocol",
](Protocol):
    async def get_by_ids(
        self,
        ids: Sequence[str] | Set[str],
        *,
        session: Session,
        batch_size: int | None = None,
        max_concurrent: int = 25,
    ) -> list[ReturnSchema]: ...


class AdderProtocol[
    CreateSchema: "BaseModel",
    ReturnSchema: "BaseModel",
    Session: "SessionProtocol",
](Protocol):
    async def add(
        self, condition: CreateSchema, *, session: Session
    ) -> ReturnSchema: ...


class UpdaterProtocol[
    UpdateSchema: "BaseModel",
    ReturnSchema: "BaseModel",
    Session: "SessionProtocol",
](Protocol):
    async def update(
        self, _id: str, condition: UpdateSchema, *, session: Session
    ) -> ReturnSchema: ...


class DeleterProtocol[Session: "SessionProtocol"](Protocol):
    async def delete(self, _id: str, *, session: Session) -> str: ...


class DeleterSoftProtocol[Session: "SessionProtocol"](Protocol):
    async def delete_soft(self, _id: str, *, session: Session) -> str: ...


class ExistedProtocol[Session: "SessionProtocol"](Protocol):
    async def exists(self, _id: str, *, session: Session) -> bool: ...


class CountProtocol[Session: "SessionProtocol"](Protocol):
    async def count(self, *, session: Session) -> int: ...


class BulkAdd[
    CreateSchema: "BaseModel",
    ReturnSchema: "BaseModel",
    Session: "SessionProtocol",
](Protocol):
    async def bulk_add(
        self, conditions: Sequence[CreateSchema], *, session: Session
    ) -> list[ReturnSchema]: ...


class BulkAddWithReturnId[
    CreateSchema: "BaseModel",
    Session: "SessionProtocol",
](Protocol):
    async def bulk_add_with_return_id(
        self, conditions: Sequence[CreateSchema], *, session: Session
    ) -> list[str]: ...


class BulkUpdate[
    UpdateSchema: "BaseModel",
    ReturnSchema: "BaseModel",
    Session: "SessionProtocol",
](Protocol):
    async def bulk_update(
        self, conditions: Sequence[UpdateSchema], *, session: Session
    ) -> list[ReturnSchema]: ...


class BulkUpdateWithReturnId[
    UpdateSchema: "BaseModel",
    Session: "SessionProtocol",
](Protocol):
    async def bulk_update_with_return_id(
        self, conditions: Sequence[UpdateSchema], *, session: Session
    ) -> list[str]: ...
