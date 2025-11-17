from typing import TYPE_CHECKING

from fastapi import status
from fastapi.responses import ORJSONResponse, Response

from common.core.exceptions import (
    BusinessLogicError,
    LockedOperationError,
    NoContentError,
)

if TYPE_CHECKING:
    from fastapi import FastAPI, Request


def register_errors_handlers(*, app: "FastAPI") -> None:
    @app.exception_handler(NoContentError)
    async def handle_no_content_error(
        request: "Request",
        exc: NoContentError,
    ) -> Response:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @app.exception_handler(LockedOperationError)
    async def handle_lock_operation_error(
        request: "Request",
        exc: LockedOperationError,
    ) -> Response:
        return Response(status_code=status.HTTP_423_LOCKED)

    @app.exception_handler(BusinessLogicError)
    async def handle_business_logic_error(
        request: "Request",
        exc: BusinessLogicError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=exc.content,
        )
