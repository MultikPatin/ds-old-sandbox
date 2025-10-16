from typing import Protocol

from common.core.protocols import (
    AdderProtocol,
    DeleterProtocol,
    SessionProtocol,
    UpdaterProtocol,
)

from src.application.dtos.db.input import (
    InputSingleDB,
    InputTableChunkDB,
    InputTableDB,
)
from src.application.dtos.input import (
    InputSingleCreate,
    InputSingleUpdate,
    InputTableChunkCreate,
    InputTableChunkUpdate,
    InputTableCreate,
    InputTableUpdate,
)


class InputSingleRepositoryProtocol[Session: SessionProtocol](
    AdderProtocol[InputSingleCreate, InputSingleDB, Session],
    UpdaterProtocol[InputSingleUpdate, InputSingleDB, Session],
    Protocol,
): ...


class InputTableRepositoryProtocol[Session: SessionProtocol](
    AdderProtocol[InputTableCreate, InputTableDB, Session],
    UpdaterProtocol[InputTableUpdate, InputTableDB, Session],
    Protocol,
):
    async def get_table_chunks_ids(
        self, _id: str, *, session: Session | None = None
    ) -> list[str]: ...


class InputTableChunkRepositoryProtocol[Session: SessionProtocol](
    AdderProtocol[InputTableChunkCreate, InputTableChunkDB, Session],
    UpdaterProtocol[InputTableChunkUpdate, InputTableChunkDB, Session],
    DeleterProtocol[Session],
    Protocol,
): ...
