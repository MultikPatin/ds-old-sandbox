from common.core.enums import ComponentsEnum
from dishka import AsyncContainer, Provider, make_async_container

from src.adapters.db.mongo import MongoProvider

from .provider import ApplicationProvider


def make_core_container(scope_component: ComponentsEnum) -> AsyncContainer:
    return make_async_container(
        make_scope_provider(scope_component),
        ApplicationProvider(),
        MongoProvider(),
    )


def make_scope_provider(scope_component: ComponentsEnum) -> Provider:
    match scope_component:
        case ComponentsEnum.fastapi:
            from dishka.integrations.fastapi import (  # noqa: PLC0415
                FastapiProvider,
            )

            return FastapiProvider()
        case ComponentsEnum.litestar:
            from dishka.integrations.litestar import (  # noqa: PLC0415
                LitestarProvider,
            )

            return LitestarProvider()
        case ComponentsEnum.faststream:
            from dishka.integrations.faststream import (  # noqa: PLC0415
                FastStreamProvider,
            )

            return FastStreamProvider()
        case _:
            raise NotImplementedError
