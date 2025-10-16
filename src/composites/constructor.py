from common.core.enums import ComponentsEnum
from common.core.protocols import APIProtocol
from dishka import AsyncContainer, make_container

from src.adapters.api.fastapi.consructor import ApiProvider
from src.application import make_core_container

scope_component = ComponentsEnum.fastapi

app = (
    make_container(
        ApiProvider(),
        context={AsyncContainer: make_core_container(scope_component)},
    )
    .get(APIProtocol)
    .api
)
