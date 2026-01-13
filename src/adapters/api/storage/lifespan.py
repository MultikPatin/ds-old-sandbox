from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from abgroup_core.protocols import InitComponentsProtocol

if TYPE_CHECKING:
    from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: "FastAPI") -> AsyncGenerator[None, None]:
    await app.state.dishka_container.get(InitComponentsProtocol)
    yield
    await app.state.dishka_container.close()
