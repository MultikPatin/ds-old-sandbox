from typing import Protocol

from abgroup_core.custom_types import AnyMatrix
from abgroup_core.protocols import (
    # AdderProtocol,
    BulkAddProtocol,
    # BulkAddWithReturnIdProtocol,
    # BulkUpdate,
    # BulkUpdateWithReturnId,
    DeleterProtocol,
    GetterByIDsProtocol,
    # DeleterProtocol,
    SessionProtocol,
    # UpdaterProtocol,
)

from src.application.dtos import (
    InputSingleCreateValuesDTO,
    InputTableCreateValuesDTO,
    InputTableWithValuesDTO,
)
from src.application.dtos.db import (
    InputSingleCreateDTO,
    InputSingleDB,
    # InputSingleUpdateDTO,
    InputTableChunkCreateDTO,
    InputTableChunkDB,
    InputTableCreateDTO,
    InputTableDB,
    # InputTableUpdateDTO,
)


class InputSingleServiceProtocol(
    # AdderProtocol[InputSingleCreateDTO, InputSingleDB, SessionProtocol],
    # UpdaterProtocol[InputSingleUpdateDTO, InputSingleDB, SessionProtocol],
    BulkAddProtocol[InputSingleCreateValuesDTO, InputSingleDB, SessionProtocol],
    # BulkAddWithReturnIdProtocol[InputSingleCreateDTO, SessionProtocol],
    # BulkUpdate[InputSingleUpdateDTO, InputSingleDB, SessionProtocol],
    # BulkUpdateWithReturnId[InputSingleUpdateDTO, SessionProtocol],
    Protocol,
): ...


class InputTableServiceProtocol(
    # AdderProtocol[InputTableCreateDTO, InputTableDB, SessionProtocol],
    # UpdaterProtocol[InputTableUpdateDTO, InputTableDB, SessionProtocol],
    BulkAddProtocol[
        InputTableCreateValuesDTO, InputTableWithValuesDTO, SessionProtocol
    ],
    # BulkAddWithReturnIdProtocol[InputTableCreateDTO, SessionProtocol],
    # BulkUpdate[InputTableUpdateDTO, InputTableDB, SessionProtocol],
    # BulkUpdateWithReturnId[InputTableUpdateDTO, SessionProtocol],
    Protocol,
): ...


class InputTableChunkServiceProtocol(Protocol):
    async def add(
        self,
        values: AnyMatrix,
        *,
        session: "SessionProtocol",
        max_concurrent: int = 25,
    ) -> list["InputTableChunkDB"]: ...


class InputSingleRepositoryProtocol[Session: SessionProtocol](
    # AdderProtocol[InputSingleCreate, InputSingleDB, Session],
    # UpdaterProtocol[InputSingleUpdate, InputSingleDB, Session],
    BulkAddProtocol[InputSingleCreateDTO, InputSingleDB, Session],
    Protocol,
): ...


class InputTableRepositoryProtocol[Session: SessionProtocol](
    # AdderProtocol[InputTableCreate, InputTableDB, Session],
    # UpdaterProtocol[InputTableUpdate, InputTableDB, Session],
    BulkAddProtocol[InputTableCreateDTO, InputTableDB, Session],
    Protocol,
): ...


class InputTableChunkRepositoryProtocol[Session: SessionProtocol](
    GetterByIDsProtocol[InputTableChunkDB, Session],
    BulkAddProtocol[InputTableChunkCreateDTO, InputTableChunkDB, Session],
    # AdderProtocol[InputTableChunkCreate, InputTableChunkDB, Session],
    # UpdaterProtocol[InputTableChunkUpdate, InputTableChunkDB, Session],
    DeleterProtocol[Session],
    Protocol,
): ...
