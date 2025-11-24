from collections.abc import AsyncGenerator

from common.core.enums import ComponentsEnum
from common.core.protocols import InitComponentProtocol, SessionProtocol
from common.mongo import Client, Settings
from dishka import Provider, Scope, alias, provide
from pymongo.asynchronous.client_session import AsyncClientSession

from src.application.dtos.db import (
    InputDB,
    InputSingleDB,
    InputTableChunkDB,
    InputTableDB,
    LayoutCardDB,
    LayoutDB,
    LayoutDefaultDB,
    LayoutSchemaDB,
    LayoutSingleDB,
    LayoutStyleDB,
    LayoutTableDB,
    LayoutValidationDB,
)
from src.application.protocols import (
    InputCardRepositoryProtocol,
    InputRepositoryProtocol,
    InputSingleRepositoryProtocol,
    InputTableChunkRepositoryProtocol,
    InputTableRepositoryProtocol,
    LayoutCardRepositoryProtocol,
    LayoutDefaultRepositoryProtocol,
    LayoutRepositoryProtocol,
    LayoutSchemaRepositoryProtocol,
    LayoutSingleRepositoryProtocol,
    LayoutStyleRepositoryProtocol,
    LayoutTableRepositoryProtocol,
    LayoutValidationRepositoryProtocol,
)

from .documents import (
    InputDocument,
    InputSingleDocument,
    InputTableChunkDocument,
    InputTableDocument,
    LayoutCardDocument,
    LayoutDefaultDocument,
    LayoutDocument,
    LayoutSchemaDocument,
    LayoutSingleDocument,
    LayoutStyleDocument,
    LayoutTableDocument,
    LayoutValidationDocument,
    collect_documents,
)
from .repositories import (
    InputCardRepository,
    InputRepository,
    InputSingleRepository,
    InputTableChunkRepository,
    InputTableRepository,
    LayoutCardRepository,
    LayoutDefaultRepository,
    LayoutRepository,
    LayoutSchemaRepository,
    LayoutSingleRepository,
    LayoutStyleRepository,
    LayoutTableRepository,
    LayoutValidationRepository,
)


class MongoProvider(Provider):
    component = ComponentsEnum.mongo

    @provide(scope=Scope.APP)
    async def init(self, client: Client) -> InitComponentProtocol:
        return InitComponentProtocol

    @provide(scope=Scope.APP)
    async def settings(self) -> Settings:
        instance = Settings()
        # TODO LOGGER Добавить логирование (debug)
        return instance

    @provide(scope=Scope.APP)
    async def client(self, settings: Settings) -> AsyncGenerator[Client, None]:
        client = Client(settings)
        documents = collect_documents()
        # TODO LOGGER Добавить логирование(debug)
        await client.initialize(documents)
        yield client
        await client.aclose()
        # TODO LOGGER Добавить логирование (debug)

    session_alias = alias(source=AsyncClientSession, provides=SessionProtocol)

    @provide(scope=Scope.REQUEST)
    async def session(
        self, client: Client
    ) -> AsyncGenerator[AsyncClientSession, None]:
        session = client.start_session()
        yield session
        await session.end_session()

    # LAYOUT

    layout_alias = alias(
        source=LayoutRepositoryProtocol[AsyncClientSession],
        provides=LayoutRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def layout(self) -> LayoutRepositoryProtocol[AsyncClientSession]:
        return LayoutRepository(LayoutDocument, LayoutDB)

    layout_card_alias = alias(
        source=LayoutCardRepositoryProtocol[AsyncClientSession],
        provides=LayoutCardRepositoryProtocol[SessionProtocol],
    )

    # LAYOUT CARD REPOSITORY

    @provide(scope=Scope.APP)
    async def layout_card(
        self,
    ) -> LayoutCardRepositoryProtocol[AsyncClientSession]:
        return LayoutCardRepository(LayoutCardDocument, LayoutCardDB)

    layout_single_alias = alias(
        source=LayoutSingleRepositoryProtocol[AsyncClientSession],
        provides=LayoutSingleRepositoryProtocol[SessionProtocol],
    )

    # LAYOUT BLOCKS

    @provide(scope=Scope.APP)
    async def layout_single(
        self,
    ) -> LayoutSingleRepositoryProtocol[AsyncClientSession]:
        return LayoutSingleRepository(LayoutSingleDocument, LayoutSingleDB)

    layout_table_alias = alias(
        source=LayoutTableRepositoryProtocol[AsyncClientSession],
        provides=LayoutTableRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def layout_table(
        self,
    ) -> LayoutTableRepositoryProtocol[AsyncClientSession]:
        return LayoutTableRepository(LayoutTableDocument, LayoutTableDB)

    layout_cell_alias = alias(
        source=LayoutSchemaRepositoryProtocol[AsyncClientSession],
        provides=LayoutSchemaRepositoryProtocol[SessionProtocol],
    )

    # LAYOUT CELLS

    @provide(scope=Scope.APP)
    async def layout_schema(
        self,
    ) -> LayoutSchemaRepositoryProtocol[AsyncClientSession]:
        return LayoutSchemaRepository(LayoutSchemaDocument, LayoutSchemaDB)

    layout_style_alias = alias(
        source=LayoutStyleRepositoryProtocol[AsyncClientSession],
        provides=LayoutStyleRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def layout_style(
        self,
    ) -> LayoutStyleRepositoryProtocol[AsyncClientSession]:
        return LayoutStyleRepository(LayoutStyleDocument, LayoutStyleDB)

    layout_validation_alias = alias(
        source=LayoutValidationRepositoryProtocol[AsyncClientSession],
        provides=LayoutValidationRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def layout_validation(
        self,
    ) -> LayoutValidationRepositoryProtocol[AsyncClientSession]:
        return LayoutValidationRepository(
            LayoutValidationDocument, LayoutValidationDB
        )

    layout_default_alias = alias(
        source=LayoutDefaultRepositoryProtocol[AsyncClientSession],
        provides=LayoutDefaultRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def layout_default(
        self,
    ) -> LayoutDefaultRepositoryProtocol[AsyncClientSession]:
        return LayoutDefaultRepository(LayoutDefaultDocument, LayoutDefaultDB)

    # INPUT

    input_alias = alias(
        source=InputRepositoryProtocol[AsyncClientSession],
        provides=InputRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def input(self) -> InputRepositoryProtocol[AsyncClientSession]:
        return InputRepository(InputDocument, InputDB)

    input_card_alias = alias(
        source=InputCardRepositoryProtocol[AsyncClientSession],
        provides=InputCardRepositoryProtocol[SessionProtocol],
    )

    # INPUT CARD

    @provide(scope=Scope.APP)
    async def input_card(
        self,
    ) -> InputCardRepositoryProtocol[AsyncClientSession]:
        return InputCardRepository(InputDocument)

    input_single_alias = alias(
        source=InputSingleRepositoryProtocol[AsyncClientSession],
        provides=InputSingleRepositoryProtocol[SessionProtocol],
    )

    # INPUT BLOCKS

    @provide(scope=Scope.APP)
    async def input_single(
        self,
    ) -> InputSingleRepositoryProtocol[AsyncClientSession]:
        return InputSingleRepository(InputSingleDocument, InputSingleDB)

    input_table_alias = alias(
        source=InputTableRepositoryProtocol[AsyncClientSession],
        provides=InputTableRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def input_table(
        self,
    ) -> InputTableRepositoryProtocol[AsyncClientSession]:
        return InputTableRepository(InputTableDocument, InputTableDB)

    input_table_chunk_alias = alias(
        source=InputTableChunkRepositoryProtocol[AsyncClientSession],
        provides=InputTableChunkRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def input_table_chunk(
        self,
    ) -> InputTableChunkRepositoryProtocol[AsyncClientSession]:
        return InputTableChunkRepository(
            InputTableChunkDocument, InputTableChunkDB
        )
