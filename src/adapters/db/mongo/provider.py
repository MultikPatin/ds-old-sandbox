from collections.abc import AsyncGenerator

from common.core.enums import ComponentsEnum
from common.core.protocols import InitComponentProtocol, SessionProtocol
from common.mongo import Client
from dishka import Provider, Scope, alias, provide
from pymongo.asynchronous.client_session import AsyncClientSession

from src.application.dtos.db.input import (
    InputDB,
    InputSingleDB,
    InputTableChunkDB,
    InputTableDB,
)
from src.application.dtos.db.layout import (
    LayoutCardDB,
    LayoutHeaderCellDB,
    LayoutRequiredCellFullLinks,
    LayoutRequiredRowFullLInks,
    LayoutSingleDB,
    LayoutStyleDB,
    LayoutTableDB,
    LayoutTooltipDB,
    LayoutValidationDB,
)
from src.application.dtos.db.model import ModelDB
from src.application.dtos.db.reference import ReferenceDB
from src.application.protocols.repositories.input import (
    InputCardRepositoryProtocol,
    InputRepositoryProtocol,
    InputSingleRepositoryProtocol,
    InputTableChunkRepositoryProtocol,
    InputTableRepositoryProtocol,
)
from src.application.protocols.repositories.key import KeyRepositoryProtocol
from src.application.protocols.repositories.layout import (
    LayoutCardRepositoryProtocol,
    LayoutHeaderCellRepositoryProtocol,
    LayoutRepositoryProtocol,
    LayoutRequiredCellRepositoryProtocol,
    LayoutRequiredRowRepositoryProtocol,
    LayoutSingleRepositoryProtocol,
    LayoutStyleRepositoryProtocol,
    LayoutTableRepositoryProtocol,
    LayoutTooltipRepositoryProtocol,
    LayoutValidationRepositoryProtocol,
)
from src.application.protocols.repositories.model import ModelRepositoryProtocol
from src.application.protocols.repositories.references import (
    ReferenceRepositoryProtocol,
)

from .documents import (
    InputsDocument,
    InputSinglesDocument,
    InputTableDocument,
    InputTablesChunksDocument,
    KeysDocument,
    LayoutCardsDocument,
    LayoutHeaderCellsDocument,
    LayoutRequiredCellsDocument,
    LayoutRequiredRowsDocument,
    LayoutsDocument,
    LayoutSinglesDocument,
    LayoutStylesDocument,
    LayoutTablesDocument,
    LayoutTooltipsDocument,
    LayoutValidationsDocument,
    ModelsDocument,
    ReferencesDocument,
    collect_documents,
)
from .repositories.input import (
    InputCardRepository,
    InputRepository,
    InputSingleRepository,
    InputTableChunkRepository,
    InputTableRepository,
)
from .repositories.key import KeyRepository
from .repositories.layout import (
    LayoutCardRepository,
    LayoutHeaderCellRepository,
    LayoutRepository,
    LayoutRequiredCellRepository,
    LayoutRequiredRowRepository,
    LayoutSingleRepository,
    LayoutStyleRepository,
    LayoutTableRepository,
    LayoutTooltipRepository,
    LayoutValidationRepository,
)
from .repositories.model import ModelRepository
from .repositories.references import ReferenceRepository
from .settings import _Settings


class MongoProvider(Provider):
    component = ComponentsEnum.mongo

    @provide(scope=Scope.APP)
    async def init(self, client: Client) -> InitComponentProtocol:
        return InitComponentProtocol

    @provide(scope=Scope.APP)
    async def settings(self) -> _Settings:
        instance = _Settings()
        # TODO LOGGER Добавить логирование (debug)
        return instance

    @provide(scope=Scope.APP)
    async def client(self, settings: _Settings) -> AsyncGenerator[Client, None]:
        client = Client(settings)
        documents = await collect_documents()
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
        session = await client.start_session()
        yield session
        await session.end_session()

    # LAYOUT REPOSITORY

    layout_alias = alias(
        source=LayoutRepositoryProtocol[AsyncClientSession],
        provides=LayoutRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def layout(self) -> LayoutRepositoryProtocol[AsyncClientSession]:
        return LayoutRepository(LayoutsDocument)

    layout_card_alias = alias(
        source=LayoutCardRepositoryProtocol[AsyncClientSession],
        provides=LayoutCardRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def layout_card(
        self,
    ) -> LayoutCardRepositoryProtocol[AsyncClientSession]:
        return LayoutCardRepository(LayoutCardsDocument, LayoutCardDB)

    layout_single_alias = alias(
        source=LayoutSingleRepositoryProtocol[AsyncClientSession],
        provides=LayoutSingleRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def layout_single(
        self,
    ) -> LayoutSingleRepositoryProtocol[AsyncClientSession]:
        return LayoutSingleRepository(LayoutSinglesDocument, LayoutSingleDB)

    layout_table_alias = alias(
        source=LayoutTableRepositoryProtocol[AsyncClientSession],
        provides=LayoutTableRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def layout_table(
        self,
    ) -> LayoutTableRepositoryProtocol[AsyncClientSession]:
        return LayoutTableRepository(LayoutTablesDocument, LayoutTableDB)

    layout_required_row_alias = alias(
        source=LayoutRequiredRowRepositoryProtocol[AsyncClientSession],
        provides=LayoutRequiredRowRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def layout_required_row(
        self,
    ) -> LayoutRequiredRowRepositoryProtocol[AsyncClientSession]:
        return LayoutRequiredRowRepository(
            LayoutRequiredRowsDocument, LayoutRequiredRowFullLInks
        )

    layout_required_cell_alias = alias(
        source=LayoutRequiredCellRepositoryProtocol[AsyncClientSession],
        provides=LayoutRequiredCellRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def layout_required_cell(
        self,
    ) -> LayoutRequiredCellRepositoryProtocol[AsyncClientSession]:
        return LayoutRequiredCellRepository(
            LayoutRequiredCellsDocument, LayoutRequiredCellFullLinks
        )

    layout_header_cell_alias = alias(
        source=LayoutHeaderCellRepositoryProtocol[AsyncClientSession],
        provides=LayoutHeaderCellRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def layout_header_cell(
        self,
    ) -> LayoutHeaderCellRepositoryProtocol[AsyncClientSession]:
        return LayoutHeaderCellRepository(
            LayoutHeaderCellsDocument, LayoutHeaderCellDB
        )

    layout_tooltip_alias = alias(
        source=LayoutTooltipRepositoryProtocol[AsyncClientSession],
        provides=LayoutTooltipRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def layout_tooltip(
        self,
    ) -> LayoutTooltipRepositoryProtocol[AsyncClientSession]:
        return LayoutTooltipRepository(LayoutTooltipsDocument, LayoutTooltipDB)

    layout_style_alias = alias(
        source=LayoutStyleRepositoryProtocol[AsyncClientSession],
        provides=LayoutStyleRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def layout_style(
        self,
    ) -> LayoutStyleRepositoryProtocol[AsyncClientSession]:
        return LayoutStyleRepository(LayoutStylesDocument, LayoutStyleDB)

    layout_validation_alias = alias(
        source=LayoutValidationRepositoryProtocol[AsyncClientSession],
        provides=LayoutValidationRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def layout_validation(
        self,
    ) -> LayoutValidationRepositoryProtocol[AsyncClientSession]:
        return LayoutValidationRepository(
            LayoutValidationsDocument, LayoutValidationDB
        )

    # INPUT REPOSITORY

    input_alias = alias(
        source=InputRepositoryProtocol[AsyncClientSession],
        provides=InputRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def input(self) -> InputRepositoryProtocol[AsyncClientSession]:
        return InputRepository(InputsDocument, InputDB)

    input_card_alias = alias(
        source=InputCardRepositoryProtocol[AsyncClientSession],
        provides=InputCardRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def input_card(
        self,
    ) -> InputCardRepositoryProtocol[AsyncClientSession]:
        return InputCardRepository(InputsDocument)

    input_single_alias = alias(
        source=InputSingleRepositoryProtocol[AsyncClientSession],
        provides=InputSingleRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def input_single(
        self,
    ) -> InputSingleRepositoryProtocol[AsyncClientSession]:
        return InputSingleRepository(InputSinglesDocument, InputSingleDB)

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
            InputTablesChunksDocument, InputTableChunkDB
        )

    # KEY REPOSITORY

    key_alias = alias(
        source=KeyRepositoryProtocol[AsyncClientSession],
        provides=KeyRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def key(self) -> KeyRepositoryProtocol[AsyncClientSession]:
        return KeyRepository(KeysDocument)

    # MODEL REPOSITORY

    model_alias = alias(
        source=ModelRepositoryProtocol[AsyncClientSession],
        provides=ModelRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def model(self) -> ModelRepositoryProtocol[AsyncClientSession]:
        return ModelRepository(ModelsDocument, ModelDB)

    # REFERENCE REPOSITORY

    reference_alias = alias(
        source=ReferenceRepositoryProtocol[AsyncClientSession],
        provides=ReferenceRepositoryProtocol[SessionProtocol],
    )

    @provide(scope=Scope.APP)
    async def reference(
        self,
    ) -> ReferenceRepositoryProtocol[AsyncClientSession]:
        return ReferenceRepository(ReferencesDocument, ReferenceDB)
