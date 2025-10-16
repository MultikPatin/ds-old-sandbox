from http import HTTPStatus

from fastapi import APIRouter

from .single import router as single_router
from .table import router as table_router

router = APIRouter()
router.include_router(
    table_router,
    prefix="/tables",
    responses={
        HTTPStatus.NO_CONTENT: {"model": None},
    },
)
router.include_router(
    single_router,
    prefix="/singles",
    responses={
        HTTPStatus.NO_CONTENT: {"model": None},
    },
)
