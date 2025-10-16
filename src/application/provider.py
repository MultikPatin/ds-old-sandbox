from typing import Annotated

from common.core.enums import ComponentsEnum
from common.core.protocols import (
    InitComponentProtocol,
    InitComponentsProtocol,
    SessionProtocol,
)
from dishka import FromComponent, Provider, Scope, provide

from src.application.protocols.repositories.input import (
    InputCardRepositoryProtocol,
    InputRepositoryProtocol,
    InputSingleRepositoryProtocol,
    InputTableChunkRepositoryProtocol,
    InputTableRepositoryProtocol,
)
from src.application.protocols.repositories.key import KeyRepositoryProtocol
from src.application.protocols.repositories.layout import (
    LayoutRepositoryProtocol,
)
from src.application.protocols.repositories.model import ModelRepositoryProtocol
from src.application.protocols.services.input import (
    InputCardServiceProtocol,
    InputServiceProtocol,
    InputSingleServiceProtocol,
    InputTableChunkServiceProtocol,
    InputTableServiceProtocol,
    InputTemplateServiceProtocol,
)
from src.application.protocols.services.layout import LayoutServiceProtocol
from src.application.protocols.services.model import ModelServiceProtocol
from src.application.services.input import (
    InputCardSrvice,
    InputService,
    InputSingleService,
    InputTableChunkService,
    InputTableService,
    InputTemplateService,
)
from src.application.services.layout import LayoutService
from src.application.services.model import ModelService

database = ComponentsEnum.mongo


class ApplicationProvider(Provider):
    @provide(scope=Scope.APP)
    async def init(
        self,
        mongo: Annotated[InitComponentProtocol, FromComponent(database)],
    ) -> InitComponentsProtocol:
        return InitComponentsProtocol

    @provide(scope=Scope.REQUEST)
    def session(
        self,
        session: Annotated[SessionProtocol, FromComponent(database)],
    ) -> SessionProtocol:
        return session

    # LAYOUT SERVICE

    @provide(scope=Scope.APP)
    def layout(
        self,
        repo: Annotated[
            LayoutRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
        input_repo: Annotated[
            InputRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
    ) -> LayoutServiceProtocol:
        return LayoutService(repo, input_repo)

    # INPUT SERVICE

    @provide(scope=Scope.APP)
    def input(
        self,
        repo: Annotated[
            InputRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
        card_service: InputCardServiceProtocol,
        single_service: InputSingleServiceProtocol,
        table_service: InputTableServiceProtocol,
    ) -> InputServiceProtocol:
        return InputService(repo, card_service, single_service, table_service)

    @provide(scope=Scope.APP)
    def input_template(
        self,
        layout_repo: Annotated[
            LayoutRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
        input_service: InputServiceProtocol,
    ) -> InputTemplateServiceProtocol:
        return InputTemplateService(layout_repo, input_service)

    @provide(scope=Scope.APP)
    def input_card(
        self,
        repo: Annotated[
            InputCardRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
        key_repo: Annotated[
            KeyRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
    ) -> InputCardServiceProtocol:
        return InputCardSrvice(repo, key_repo)

    @provide(scope=Scope.APP)
    def input_single(
        self,
        repo: Annotated[
            InputSingleRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
    ) -> InputSingleServiceProtocol:
        return InputSingleService(repo)

    @provide(scope=Scope.APP)
    def input_table(
        self,
        repo: Annotated[
            InputTableRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
        chunk_service: InputTableChunkServiceProtocol,
    ) -> InputTableServiceProtocol:
        return InputTableService(repo, chunk_service)

    @provide(scope=Scope.APP)
    def input_table_chunk(
        self,
        repo: Annotated[
            InputTableChunkRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
    ) -> InputTableChunkServiceProtocol:
        return InputTableChunkService(repo)

    # MODEL SERVICE

    @provide(scope=Scope.APP)
    def model(
        self,
        repo: Annotated[
            ModelRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
        key_repo: Annotated[
            KeyRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
    ) -> ModelServiceProtocol:
        return ModelService(repo, key_repo)
