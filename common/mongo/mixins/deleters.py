from typing import TYPE_CHECKING

from abgroup_core.enums import LifeStatusEnum
from abgroup_core.exceptions import (
    LockedOperationError,
    LockedOperationErrorContent,
)
from abgroup_core.utils import time_now

from .getters import _GetMixin

if TYPE_CHECKING:
    from pymongo.asynchronous.client_session import AsyncClientSession


class DeleteMixin(_GetMixin):
    async def delete(self, _id: str, *, session: "AsyncClientSession") -> str:
        document = await self._get(_id, session=session)
        await document.delete(session=session)
        return _id


class DeleteWithRefCountMixin(_GetMixin):
    async def delete(self, _id: str, *, session: "AsyncClientSession") -> str:
        document = await self._get(_id, session=session)
        if not hasattr(document, "ref_count"):
            msg = "Document has no ref_count attribute"
            raise AttributeError(msg)

        if document.ref_count > 0:
            raise LockedOperationError(
                LockedOperationErrorContent(
                    message="An object cannot be deleted while "
                    "it is referenced by other objects",
                    context={"ref_count": document.ref_count},
                )
            )

        await document.delete(session=session)
        return _id


class DeleteSoftMixin(_GetMixin):
    async def delete_soft(
        self, _id: str, *, session: "AsyncClientSession"
    ) -> str:
        document = await self._get(_id, session=session)

        if not hasattr(document, "status"):
            msg = "Document has no status attribute"
            raise AssertionError(msg)
        if not isinstance(document.status, LifeStatusEnum):
            msg = "Status attribute is not an instance of LifeStatusEnum"
            raise TypeError(msg)

        document.status = LifeStatusEnum.deleted

        # TODO: конкретизировать назначение и тип полей
        if hasattr(document, "deleted_at"):
            document.deleted_at = time_now()
        if hasattr(document, "deleted"):
            if isinstance(document.deleted, bool):
                document.deleted = True
            else:
                document.deleted = time_now()
        if hasattr(document, "updated_at"):
            document.updated_at = time_now()
        if hasattr(document, "updated"):
            if isinstance(document.updated, bool):
                document.updated = True
            else:
                document.updated = time_now()
        await document.save_changes(session=session)
        return _id
