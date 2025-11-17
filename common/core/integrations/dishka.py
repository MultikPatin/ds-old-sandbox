try:
    from dishka import Provider
except ImportError:
    msg = (
        "To use dishka integration, "
        "install the library using the extra dependencies"
    )
    raise ImportError(msg)

from common.core.enums import ComponentsEnum


def scope_provider(scope: ComponentsEnum) -> Provider:
    match scope:
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
