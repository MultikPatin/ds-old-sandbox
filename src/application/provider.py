from typing import Annotated

from abgroup_core.enums import ComponentsEnum
from abgroup_core.protocols import (
    InitComponentProtocol,
    InitComponentsProtocol,
    SessionProtocol,
)
from dishka import FromComponent, Provider, Scope, provide

from src.application.protocols import (
    InputCardRepositoryProtocol,
    InputCardServiceProtocol,
    InputRepositoryProtocol,
    InputServiceProtocol,
    InputSingleRepositoryProtocol,
    InputSingleServiceProtocol,
    InputTableChunkRepositoryProtocol,
    InputTableChunkServiceProtocol,
    InputTableRepositoryProtocol,
    InputTableServiceProtocol,
    InputToolsServiceProtocol,
    LayoutBlocksFetcherProtocol,
    LayoutDefaultRepositoryProtocol,
    LayoutDefaultServiceProtocol,
    LayoutMessageRepositoryProtocol,
    LayoutMessageServiceProtocol,
    LayoutRepositoryProtocol,
    LayoutSchemaRepositoryProtocol,
    LayoutSchemaServiceProtocol,
    LayoutServiceProtocol,
    LayoutSingleRepositoryProtocol,
    LayoutSingleServiceProtocol,
    LayoutStyleRepositoryProtocol,
    LayoutStyleServiceProtocol,
    LayoutTableRepositoryProtocol,
    LayoutTableServiceProtocol,
    LayoutValidationRepositoryProtocol,
    LayoutValidationServiceProtocol,
)
from src.application.services import (
    InputCardSrvice,
    InputService,
    InputSingleService,
    InputTableChunkService,
    InputTableService,
    InputToolsService,
    LayoutBlocksFetcher,
    LayoutDefaultService,
    LayoutMessageService,
    LayoutSchemaService,
    LayoutService,
    LayoutSingleService,
    LayoutStyleService,
    LayoutTableService,
    LayoutValidationService,
)

database = ComponentsEnum.mongo


class _InputProvider(Provider):
    @provide(scope=Scope.APP)
    def __input(
        self,
        repo: Annotated[
            InputRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
        # card_service: InputCardServiceProtocol,
        single_service: InputSingleServiceProtocol,
        table_service: InputTableServiceProtocol,
        tools_service: InputToolsServiceProtocol,
    ) -> InputServiceProtocol:
        return InputService(
            repo,
            # card_service=card_service,
            single_service=single_service,
            table_service=table_service,
            tools_service=tools_service,
        )

    @provide(scope=Scope.APP)
    def __tools(
        self,
        layout_service: LayoutServiceProtocol,
        table_chunk_repo: Annotated[
            InputTableChunkRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
    ) -> InputToolsServiceProtocol:
        return InputToolsService(
            layout_service=layout_service,
            table_chunk_repo=table_chunk_repo,
        )

    # BLOCKS

    @provide(scope=Scope.APP)
    def __card(
        self,
        repo: Annotated[
            InputCardRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
        layout_service: LayoutServiceProtocol,
    ) -> InputCardServiceProtocol:
        return InputCardSrvice(
            repo,
            layout_service=layout_service,
        )

    @provide(scope=Scope.APP)
    def __single(
        self,
        repo: Annotated[
            InputSingleRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
    ) -> InputSingleServiceProtocol:
        return InputSingleService(repo)

    @provide(scope=Scope.APP)
    def __table(
        self,
        repo: Annotated[
            InputTableRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
        chunk_service: InputTableChunkServiceProtocol,
    ) -> InputTableServiceProtocol:
        return InputTableService(repo, chunk_service)

    @provide(scope=Scope.APP)
    def __table_chunk(
        self,
        repo: Annotated[
            InputTableChunkRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
    ) -> InputTableChunkServiceProtocol:
        return InputTableChunkService(repo)


class _LayoutProvider(Provider):
    @provide(scope=Scope.APP)
    def __fetcher(
        self,
        schema_repo: Annotated[
            LayoutSchemaRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
        style_repo: Annotated[
            LayoutStyleRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
        validation_repo: Annotated[
            LayoutValidationRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
        default_repo: Annotated[
            LayoutDefaultRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
    ) -> LayoutBlocksFetcherProtocol:
        return LayoutBlocksFetcher(
            schema_repo=schema_repo,
            style_repo=style_repo,
            validation_repo=validation_repo,
            default_repo=default_repo,
        )

    @provide(scope=Scope.APP)
    def __layout(
        self,
        repo: Annotated[
            LayoutRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
        input_repo: Annotated[
            InputRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
        fetcher_service: "LayoutBlocksFetcherProtocol",
    ) -> LayoutServiceProtocol:
        return LayoutService(
            repo,
            input_repo=input_repo,
            fetcher_service=fetcher_service,
        )

    # BLOCKS

    @provide(scope=Scope.APP)
    def __single(
        self,
        repo: Annotated[
            LayoutSingleRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
        fetcher_service: "LayoutBlocksFetcherProtocol",
    ) -> LayoutSingleServiceProtocol:
        return LayoutSingleService(
            repo,
            fetcher_service=fetcher_service,
        )

    @provide(scope=Scope.APP)
    def __table(
        self,
        repo: Annotated[
            LayoutTableRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
        fetcher_service: "LayoutBlocksFetcherProtocol",
    ) -> LayoutTableServiceProtocol:
        return LayoutTableService(
            repo,
            fetcher_service=fetcher_service,
        )

    @provide(scope=Scope.APP)
    def __message(
        self,
        repo: Annotated[
            LayoutMessageRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
    ) -> LayoutMessageServiceProtocol:
        return LayoutMessageService(repo)

    # LAYERS

    @provide(scope=Scope.APP)
    def __schema(
        self,
        repo: Annotated[
            LayoutSchemaRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
    ) -> LayoutSchemaServiceProtocol:
        return LayoutSchemaService(repo)

    @provide(scope=Scope.APP)
    def __style(
        self,
        repo: Annotated[
            LayoutStyleRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
    ) -> LayoutStyleServiceProtocol:
        return LayoutStyleService(repo)

    @provide(scope=Scope.APP)
    def __validation(
        self,
        repo: Annotated[
            LayoutValidationRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
    ) -> LayoutValidationServiceProtocol:
        return LayoutValidationService(repo)

    @provide(scope=Scope.APP)
    def __default(
        self,
        repo: Annotated[
            LayoutDefaultRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
    ) -> LayoutDefaultServiceProtocol:
        return LayoutDefaultService(repo)


class _ApplicationProvider(Provider):
    @provide(scope=Scope.APP)
    async def __init(
        self,
        mongo: Annotated[InitComponentProtocol, FromComponent(database)],
    ) -> InitComponentsProtocol:
        return InitComponentsProtocol

    @provide(scope=Scope.REQUEST)
    def __session(
        self,
        session: Annotated[SessionProtocol, FromComponent(database)],
    ) -> SessionProtocol:
        return session


class ApplicationProvider(
    _InputProvider, _LayoutProvider, _ApplicationProvider
):
    pass
