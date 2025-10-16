from typing import Protocol

from common.core.enums import LifeStatusEnum
from common.core.protocols import (
    AdderProtocol,
    DeleterProtocol,
    GetterProtocol,
    SessionProtocol,
    UpdaterProtocol,
)

from src.application.dtos.db.input import (
    InputCreateDTO,
    InputUpdateDTO,
    InputWithTableInMatrix,
)


class InputServiceProtocol(
    GetterProtocol[InputWithTableInMatrix, SessionProtocol],
    AdderProtocol[InputCreateDTO, InputWithTableInMatrix, SessionProtocol],
    UpdaterProtocol[InputUpdateDTO, InputWithTableInMatrix, SessionProtocol],
    DeleterProtocol[SessionProtocol],
    Protocol,
):
    async def update_status(
        self,
        _id: str,
        status: LifeStatusEnum,
        *,
        session: SessionProtocol | None = None,
    ) -> LifeStatusEnum: ...
