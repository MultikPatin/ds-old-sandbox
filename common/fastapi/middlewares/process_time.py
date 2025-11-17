import time
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING

from starlette.middleware.base import BaseHTTPMiddleware

if TYPE_CHECKING:
    from fastapi import Request, Response
    from starlette.types import ASGIApp

type CallNext = Callable[["Request"], Awaitable["Response"]]


class ProcessTimeHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: "ASGIApp",
        header_name: str,
    ) -> None:
        super().__init__(app=app)
        self.header_name = header_name

    async def dispatch(
        self, request: "Request", call_next: CallNext
    ) -> "Response":
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        in_ms = process_time * 1000
        response.headers[self.header_name] = f"{in_ms:.3f} ms"
        return response
