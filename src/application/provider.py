from typing import Annotated

from common.core.enums import ComponentsEnum
from common.core.protocols import (
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
    InputTableChunkRepositoryProtocol,
    InputTableChunkServiceProtocol,
    InputToolsServiceProtocol,
    LayoutRepositoryProtocol,
    LayoutSchemaRepositoryProtocol,
    LayoutSchemaServiceProtocol,
    LayoutServiceProtocol,
    LayoutStyleRepositoryProtocol,
    LayoutStyleServiceProtocol,
    LayoutValidationRepositoryProtocol,
    LayoutValidationServiceProtocol,
)
from src.application.services import (
    InputCardSrvice,
    InputService,
    InputTableChunkService,
    InputToolsService,
    #     InputTableService,
    #     InputTemplateService,
    LayoutSchemaService,
    LayoutService,
    LayoutStyleService,
    LayoutValidationService,
)

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

    # LAYOUT

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
        cell_schema_service: LayoutSchemaServiceProtocol,
        cell_style_service: LayoutStyleServiceProtocol,
        cell_validation_service: LayoutValidationServiceProtocol,
    ) -> LayoutServiceProtocol:
        return LayoutService(
            repo,
            input_repo=input_repo,
            cell_schema_service=cell_schema_service,
            cell_style_service=cell_style_service,
            cell_validation_service=cell_validation_service,
        )

    # LAYOUT CELLS

    @provide(scope=Scope.APP)
    def layout_schema(
        self,
        repo: Annotated[
            LayoutSchemaRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
    ) -> LayoutSchemaServiceProtocol:
        return LayoutSchemaService(repo)

    @provide(scope=Scope.APP)
    def layout_style(
        self,
        repo: Annotated[
            LayoutStyleRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
    ) -> LayoutStyleServiceProtocol:
        return LayoutStyleService(repo)

    @provide(scope=Scope.APP)
    def layout_validation(
        self,
        repo: Annotated[
            LayoutValidationRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
    ) -> LayoutValidationServiceProtocol:
        return LayoutValidationService(repo)

    # INPUT SERVICE

    @provide(scope=Scope.APP)
    def input(
        self,
        repo: Annotated[
            InputRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
        # card_service: InputCardServiceProtocol,
        # single_service: InputSingleServiceProtocol,
        # table_service: InputTableServiceProtocol,
        table_chunk_service: InputTableChunkServiceProtocol,
        tools_service: "InputToolsServiceProtocol",
    ) -> InputServiceProtocol:
        return InputService(
            repo,
            # card_service=card_service,
            # single_service=single_service,
            # table_service=table_service,
            table_chunk_service=table_chunk_service,
            tools_service=tools_service,
        )

    @provide(scope=Scope.APP)
    def input_tools(
        self,
        layout_service: LayoutServiceProtocol,
    ) -> InputToolsServiceProtocol:
        return InputToolsService(layout_service)

    @provide(scope=Scope.APP)
    def input_card(
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

    # @provide(scope=Scope.APP)
    # def input_single(
    #     self,
    #     repo: Annotated[
    #         InputSingleRepositoryProtocol[SessionProtocol],
    #         FromComponent(database),
    #     ],
    # ) -> InputSingleServiceProtocol:
    #     return InputSingleService(repo)
    #
    # @provide(scope=Scope.APP)
    # def input_table(
    #     self,
    #     repo: Annotated[
    #         InputTableRepositoryProtocol[SessionProtocol],
    #         FromComponent(database),
    #     ],
    #     chunk_service: InputTableChunkServiceProtocol,
    # ) -> InputTableServiceProtocol:
    #     return InputTableService(repo, chunk_service)
    #
    @provide(scope=Scope.APP)
    def input_table_chunk(
        self,
        repo: Annotated[
            InputTableChunkRepositoryProtocol[SessionProtocol],
            FromComponent(database),
        ],
    ) -> InputTableChunkServiceProtocol:
        return InputTableChunkService(repo)
