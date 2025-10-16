from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from common.core.protocols import InitComponentsProtocol
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await app.state.dishka_container.get(InitComponentsProtocol)
    yield
    await app.state.dishka_container.close()
