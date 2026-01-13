from dishka import AsyncContainer, Provider, make_async_container

from src.adapters.db.mongo import MongoProvider

from .provider import ApplicationProvider


def make_core_container(
    scope_provider: Provider | None = None,
) -> AsyncContainer:
    providers: list[Provider] = [
        ApplicationProvider(),
        MongoProvider(),
    ]
    if scope_provider is not None:
        providers.append(scope_provider)
    return make_async_container(*providers)
