from abgroup_core.protocols import MAppProtocol
from abgroup_fastapi import MApp
from dishka import AsyncContainer, Provider, Scope, from_context, provide
from dishka.integrations.fastapi import setup_dishka

from . import v1
from .lifespan import lifespan
from .settings import Settings


class ApiProvider(Provider):
    container = from_context(provides=AsyncContainer, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def settings(self) -> Settings:
        # TODO LOGGER Добавить логирование (debug)
        return Settings()

    @provide(scope=Scope.APP)
    def app(
        self, settings: Settings, container: AsyncContainer, api_v1: v1.App
    ) -> MAppProtocol:
        app = MApp(settings, lifespan)
        setup_dishka(container=container, app=app.api)
        app.mount(api_v1)
        return app

    @provide(scope=Scope.APP)
    def settings_v1(self) -> v1.Settings:
        # TODO LOGGER Добавить логирование (debug)
        return v1.Settings()

    @provide(scope=Scope.APP)
    def api_v1(self, app_settings: Settings, settings: v1.Settings) -> v1.App:
        return v1.App(
            is_dev_mode=app_settings.IS_DEV_MODE,
            settings=settings,
        )
