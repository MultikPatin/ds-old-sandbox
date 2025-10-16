from typing import Protocol

from common.core.custom_types import AnyMatrix
from common.core.protocols import (
    AdderProtocol,
    BulkAdd,
    BulkAddWithReturnId,
    BulkUpdate,
    BulkUpdateWithReturnId,
    DeleterProtocol,
    SessionProtocol,
    UpdaterProtocol,
)

from src.application.dtos.db.input import (
    InputSingleCreateDTO,
    InputSingleDB,
    InputSingleUpdateDTO,
    InputTableChunkDB,
    InputTableCreateDTO,
    InputTableDB,
    InputTableUpdateDTO,
)
from src.application.dtos.input import (
    InputTableChunkCreate,
    InputTableChunkUpdate,
)


class InputSingleServiceProtocol(
    AdderProtocol[InputSingleCreateDTO, InputSingleDB, SessionProtocol],
    UpdaterProtocol[InputSingleUpdateDTO, InputSingleDB, SessionProtocol],
    BulkAdd[InputSingleCreateDTO, InputSingleDB, SessionProtocol],
    BulkAddWithReturnId[InputSingleCreateDTO, SessionProtocol],
    BulkUpdate[InputSingleUpdateDTO, InputSingleDB, SessionProtocol],
    BulkUpdateWithReturnId[InputSingleUpdateDTO, SessionProtocol],
    Protocol,
): ...


class InputTableServiceProtocol(
    AdderProtocol[InputTableCreateDTO, InputTableDB, SessionProtocol],
    UpdaterProtocol[InputTableUpdateDTO, InputTableDB, SessionProtocol],
    BulkAdd[InputTableCreateDTO, InputTableDB, SessionProtocol],
    BulkAddWithReturnId[InputTableCreateDTO, SessionProtocol],
    BulkUpdate[InputTableUpdateDTO, InputTableDB, SessionProtocol],
    BulkUpdateWithReturnId[InputTableUpdateDTO, SessionProtocol],
    Protocol,
): ...


class InputTableChunkServiceProtocol(
    AdderProtocol[InputTableChunkCreate, InputTableChunkDB, SessionProtocol],
    UpdaterProtocol[InputTableChunkUpdate, InputTableChunkDB, SessionProtocol],
    DeleterProtocol[SessionProtocol],
    Protocol,
):
    async def add_from_matrix(
        self, matrix: AnyMatrix, *, session: SessionProtocol | None = None
    ) -> list[InputTableChunkDB]: ...
    async def rebuild_chunks(
        self,
        chuck_ids: list[str],
        matrix: AnyMatrix,
        *,
        session: SessionProtocol | None = None,
    ) -> list[InputTableChunkDB]: ...
