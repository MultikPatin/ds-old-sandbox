from typing import Protocol

# from common.core.custom_types import AnyMatrix
from common.core.protocols import (
    AdderProtocol,
    BulkAdd,
    BulkAddWithReturnId,
    BulkUpdate,
    BulkUpdateWithReturnId,
    DeleterProtocol,
    GetterByIDsProtocol,
    # DeleterProtocol,
    SessionProtocol,
    UpdaterProtocol,
)

from src.application.dtos.db import (
    InputSingleCreateDTO,
    InputSingleDB,
    InputSingleUpdateDTO,
    InputTableChunkDB,
    InputTableCreateDTO,
    InputTableDB,
    InputTableUpdateDTO,
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
    GetterByIDsProtocol[InputTableChunkDB, SessionProtocol],
    # AdderProtocol[InputTableChunkCreate, InputTableChunkDB, SessionProtocol],
    # UpdaterProtocol[InputTableChunkUpdate, InputTableChunkDB, SessionProtocol],
    # DeleterProtocol[SessionProtocol],
    Protocol,
): ...


class InputSingleRepositoryProtocol[Session: SessionProtocol](
    # AdderProtocol[InputSingleCreate, InputSingleDB, Session],
    # UpdaterProtocol[InputSingleUpdate, InputSingleDB, Session],
    Protocol,
): ...


class InputTableRepositoryProtocol[Session: SessionProtocol](
    # AdderProtocol[InputTableCreate, InputTableDB, Session],
    # UpdaterProtocol[InputTableUpdate, InputTableDB, Session],
    Protocol,
):
    ...
    # async def get_table_chunks_ids(
    #     self, _id: str, *, session: Session | None = None
    # ) -> list[str]: ...


class InputTableChunkRepositoryProtocol[Session: SessionProtocol](
    GetterByIDsProtocol[InputTableChunkDB, Session],
    # AdderProtocol[InputTableChunkCreate, InputTableChunkDB, Session],
    # UpdaterProtocol[InputTableChunkUpdate, InputTableChunkDB, Session],
    DeleterProtocol[Session],
    Protocol,
): ...
