from abgroup_core.protocols import MAppProtocol
from dishka import AsyncContainer, make_container
from dishka.integrations.fastapi import FastapiProvider

from src.adapters.api.storage import ApiProvider
from src.application import make_core_container

app = (
    make_container(
        ApiProvider(),
        context={
            AsyncContainer: make_core_container(FastapiProvider()),
        },
    )
    .get(MAppProtocol)
    .api
)
