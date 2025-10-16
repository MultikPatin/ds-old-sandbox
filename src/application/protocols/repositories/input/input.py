from typing import Protocol

from common.core.enums import LifeStatusEnum
from common.core.protocols import (
    AdderProtocol,
    DeleterProtocol,
    SessionProtocol,
)

from src.application.dtos.db.input import (
    InputDB,
    InputFullLinks,
    InputUpdateDTO,
)
from src.application.dtos.input import InputCreate


class InputRepositoryProtocol[Session: SessionProtocol](
    AdderProtocol[InputCreate, InputDB, Session],
    DeleterProtocol[Session],
    Protocol,
):
    async def get_full_links(
        self, _id: str, *, session: Session | None = None
    ) -> InputFullLinks: ...
    async def update_full_links(
        self,
        _id: str,
        condition: InputUpdateDTO,
        *,
        session: Session | None = None,
    ) -> InputFullLinks: ...
    async def get_layout_id(
        self, _id: str, *, session: Session | None = None
    ) -> str: ...
    async def update_status(
        self,
        _id: str,
        status: LifeStatusEnum,
        *,
        session: Session | None = None,
    ) -> str: ...
