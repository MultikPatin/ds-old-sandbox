from common.core.enums import ComponentsEnum
from common.core.protocols import MAppProtocol
from dishka import AsyncContainer, make_container

from src.adapters.api.storage import ApiProvider
from src.application import make_core_container

app = (
    make_container(
        ApiProvider(),
        context={AsyncContainer: make_core_container(ComponentsEnum.fastapi)},
    )
    .get(MAppProtocol)
    .api
)
