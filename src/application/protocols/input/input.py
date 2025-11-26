from typing import TYPE_CHECKING, Protocol

from common.core.protocols import (
    AdderProtocol,
    DeleterSoftProtocol,
    # UpdaterProtocol,
    # DeleterProtocol,
    GetterProtocol,
    SessionProtocol,
)

from src.application.dtos.db import (
    InputCreateDTO,
    # InputUpdateDTO,
    InputDB,
)

if TYPE_CHECKING:
    from common.core.enums import LifeStatusEnum

    from src.application.dtos import InputWithValuesDTO
    from src.application.dtos.db.input import InputWithBlocks


class _GetFullLinks[Session: SessionProtocol](Protocol):
    async def get_full_links(
        self, _id: str, *, session: Session
    ) -> "InputWithBlocks": ...


class InputServiceProtocol(
    GetterProtocol[InputDB, SessionProtocol],
    # UpdaterProtocol[InputUpdateDTO, InputFullLinks, SessionProtocol],
    DeleterSoftProtocol[SessionProtocol],
    _GetFullLinks[SessionProtocol],
    Protocol,
):
    async def add_as_template(
        self, layout_key: str, *, session: SessionProtocol
    ) -> "InputWithValuesDTO": ...
    async def get_with_values(
        self, _id: str, *, session: SessionProtocol
    ) -> "InputWithValuesDTO": ...
    async def update_status(
        self, _id: str, status: "LifeStatusEnum", *, session: SessionProtocol
    ) -> "LifeStatusEnum": ...


class InputRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[InputDB, Session],
    AdderProtocol[InputCreateDTO, InputDB, Session],
    DeleterSoftProtocol[Session],
    _GetFullLinks[Session],
    Protocol,
):
    async def get_layout_id(self, _id: str, *, session: Session) -> str: ...
    async def update_status(
        self, _id: str, status: "LifeStatusEnum", *, session: Session
    ) -> None: ...

    # async def update_full_links(
    #     self,
    #     _id: str,
    #     condition: InputUpdateDTO,
    #     *,
    #     session: Session | None = None,
    # ) -> InputFullLinks: ...
