from common.core.protocols import APIProtocol
from dishka import AsyncContainer, Provider, Scope, from_context, provide
from dishka.integrations.fastapi import setup_dishka

from . import v1
from .app import _App
from .lifespan import lifespan
from .settings import Settings


class ApiProvider(Provider):
    @provide(scope=Scope.APP)
    def settings(self) -> Settings:
        instance = Settings()
        # TODO LOGGER Добавить логирование (debug)
        return instance

    @provide(scope=Scope.APP)
    def v1_settings(self) -> v1.Settings:
        instance = v1.Settings()
        # TODO LOGGER Добавить логирование (debug)
        return instance

    container = from_context(provides=AsyncContainer, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def app(
        self, settings: Settings, container: AsyncContainer, api_v1: v1.App
    ) -> APIProtocol:
        app = _App(settings, lifespan)
        setup_dishka(container=container, app=app.api)
        app.mount(api_v1)
        return app

    @provide(scope=Scope.APP)
    def api_v1(self, app_settings: Settings, settings: v1.Settings) -> v1.App:
        return v1.App(
            is_dev_mode=app_settings.IS_DEV_MODE,
            settings=settings,
        )
