from common.core.enums import ComponentsEnum
from common.core.integrations.dishka import scope_provider
from dishka import AsyncContainer, Provider, make_async_container

from src.adapters.db.mongo import MongoProvider

from .provider import ApplicationProvider


def make_core_container(
    scope: ComponentsEnum | None = None,
) -> AsyncContainer:
    providers: list[Provider] = [
        ApplicationProvider(),
        MongoProvider(),
    ]
    if scope is not None:
        providers.append(scope_provider(scope))
    return make_async_container(*providers)
