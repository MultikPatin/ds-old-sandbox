from collections.abc import AsyncGenerator

from abgroup_core.enums import ComponentsEnum
from abgroup_core.protocols import InitComponentProtocol, SessionProtocol
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
    LayoutMessageDB,
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
    LayoutMessageRepositoryProtocol,
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
    LayoutMessageDocument,
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
    LayoutMessageRepository,
    LayoutRepository,
    LayoutSchemaRepository,
    LayoutSingleRepository,
    LayoutStyleRepository,
    LayoutTableRepository,
    LayoutValidationRepository,
)


class _InputProvider(Provider):
    __input_alias = alias(
        source=InputRepositoryProtocol[AsyncClientSession],
        provides=InputRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def __input(self) -> InputRepositoryProtocol[AsyncClientSession]:
        return InputRepository(InputDocument, InputDB)

    # BLOCKS

    __card_alias = alias(
        source=InputCardRepositoryProtocol[AsyncClientSession],
        provides=InputCardRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def __card(
        self,
    ) -> InputCardRepositoryProtocol[AsyncClientSession]:
        return InputCardRepository(InputDocument)

    __single_alias = alias(
        source=InputSingleRepositoryProtocol[AsyncClientSession],
        provides=InputSingleRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def __single(
        self,
    ) -> InputSingleRepositoryProtocol[AsyncClientSession]:
        return InputSingleRepository(InputSingleDocument, InputSingleDB)

    __table_alias = alias(
        source=InputTableRepositoryProtocol[AsyncClientSession],
        provides=InputTableRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def __table(
        self,
    ) -> InputTableRepositoryProtocol[AsyncClientSession]:
        return InputTableRepository(InputTableDocument, InputTableDB)

    __table_chunk_alias = alias(
        source=InputTableChunkRepositoryProtocol[AsyncClientSession],
        provides=InputTableChunkRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def __table_chunk(
        self,
    ) -> InputTableChunkRepositoryProtocol[AsyncClientSession]:
        return InputTableChunkRepository(
            InputTableChunkDocument, InputTableChunkDB
        )


class _LayoutProvider(Provider):
    __layout_alias = alias(
        source=LayoutRepositoryProtocol[AsyncClientSession],
        provides=LayoutRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def __layout(self) -> LayoutRepositoryProtocol[AsyncClientSession]:
        return LayoutRepository(LayoutDocument, LayoutDB)

    # BLOCKS

    __card_alias = alias(
        source=LayoutCardRepositoryProtocol[AsyncClientSession],
        provides=LayoutCardRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def __card(
        self,
    ) -> LayoutCardRepositoryProtocol[AsyncClientSession]:
        return LayoutCardRepository(LayoutCardDocument, LayoutCardDB)

    __single_alias = alias(
        source=LayoutSingleRepositoryProtocol[AsyncClientSession],
        provides=LayoutSingleRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def __single(
        self,
    ) -> LayoutSingleRepositoryProtocol[AsyncClientSession]:
        return LayoutSingleRepository(LayoutSingleDocument, LayoutSingleDB)

    __table_alias = alias(
        source=LayoutTableRepositoryProtocol[AsyncClientSession],
        provides=LayoutTableRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def __table(
        self,
    ) -> LayoutTableRepositoryProtocol[AsyncClientSession]:
        return LayoutTableRepository(LayoutTableDocument, LayoutTableDB)

    __message_alias = alias(
        source=LayoutMessageRepositoryProtocol[AsyncClientSession],
        provides=LayoutMessageRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def __message(
        self,
    ) -> LayoutMessageRepositoryProtocol[AsyncClientSession]:
        return LayoutMessageRepository(LayoutMessageDocument, LayoutMessageDB)

    # LAYERS

    __schema_alias = alias(
        source=LayoutSchemaRepositoryProtocol[AsyncClientSession],
        provides=LayoutSchemaRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def __schema(
        self,
    ) -> LayoutSchemaRepositoryProtocol[AsyncClientSession]:
        return LayoutSchemaRepository(LayoutSchemaDocument, LayoutSchemaDB)

    __style_alias = alias(
        source=LayoutStyleRepositoryProtocol[AsyncClientSession],
        provides=LayoutStyleRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def __style(
        self,
    ) -> LayoutStyleRepositoryProtocol[AsyncClientSession]:
        return LayoutStyleRepository(LayoutStyleDocument, LayoutStyleDB)

    __validation_alias = alias(
        source=LayoutValidationRepositoryProtocol[AsyncClientSession],
        provides=LayoutValidationRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def __validation(
        self,
    ) -> LayoutValidationRepositoryProtocol[AsyncClientSession]:
        return LayoutValidationRepository(
            LayoutValidationDocument, LayoutValidationDB
        )

    __default_alias = alias(
        source=LayoutDefaultRepositoryProtocol[AsyncClientSession],
        provides=LayoutDefaultRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def __default(
        self,
    ) -> LayoutDefaultRepositoryProtocol[AsyncClientSession]:
        return LayoutDefaultRepository(LayoutDefaultDocument, LayoutDefaultDB)


class _MongoProvider(Provider):
    component = ComponentsEnum.mongo

    @provide(scope=Scope.APP)
    async def __init(self, client: Client) -> InitComponentProtocol:
        return InitComponentProtocol

    @provide(scope=Scope.APP)
    async def __settings(self) -> Settings:
        # TODO LOGGER Добавить логирование (debug)
        return Settings()

    @provide(scope=Scope.APP)
    async def __client(
        self, settings: Settings
    ) -> AsyncGenerator[Client, None]:
        client = Client(settings)
        documents = collect_documents()
        # TODO LOGGER Добавить логирование(debug)
        await client.initialize(documents)
        yield client
        await client.aclose()
        # TODO LOGGER Добавить логирование (debug)

    __session_alias = alias(source=AsyncClientSession, provides=SessionProtocol)

    @provide(scope=Scope.REQUEST)
    async def __session(
        self, client: Client
    ) -> AsyncGenerator[AsyncClientSession, None]:
        session = client.start_session()
        yield session
        await session.end_session()


class MongoProvider(_InputProvider, _LayoutProvider, _MongoProvider):
    pass
