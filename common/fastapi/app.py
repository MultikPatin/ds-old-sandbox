from typing import TYPE_CHECKING

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse
from starlette.types import Lifespan

from common.core.constants import (
    API_DEFAULT_ROOT_PATH,
    API_HEADER_PROCESS_TIME,
)
from common.core.enums import URLEnum

from .base import MBaseApp, VBaseApp
from .errors_handlers import register_errors_handlers
from .middlewares import ProcessTimeHeaderMiddleware
from .static_docs import register as register_static_docs

if TYPE_CHECKING:
    from common.core.protocols import VAppProtocol

    from .settings import MSettings, VSettings


class MApp(MBaseApp):
    def __init__[Settings: "MSettings"](
        self,
        settings: Settings,
        lifespan: Lifespan[FastAPI] | None = None,
    ):
        self._api = FastAPI(
            default_response_class=ORJSONResponse,
            lifespan=lifespan,
            docs_url=None,
            redoc_url=None,
            openapi_url=None,
            root_path=API_DEFAULT_ROOT_PATH,
        )
        if settings.IS_DEV_MODE:
            self._api.add_middleware(
                ProcessTimeHeaderMiddleware,
                header_name=API_HEADER_PROCESS_TIME,
            )
        self._api.add_middleware(
            CORSMiddleware,
            allow_origins=settings.ALLOW_ORIGINS,
            allow_headers=settings.ALLOW_HEADERS,
            allow_methods=settings.ALLOW_METHODS,
        )
        if settings.IS_GZIP:
            self._api.add_middleware(
                GZipMiddleware,
                minimum_size=settings.GZIP_MIN_SIZE,
                compresslevel=settings.GZIP_COMPRESS_LEVEL,
            )

    def mount(self, app: "VAppProtocol") -> None:
        self._api.mount(path=app.path, app=app.api)


class VApp(VBaseApp):
    def __init__[Settings: "VSettings"](
        self,
        is_dev_mode: bool,
        settings: Settings,
    ) -> None:
        self._path = settings.path
        docs_url = (
            None if settings.IS_STATIC_DOCS or not is_dev_mode else URLEnum.docs
        )

        self._api = FastAPI(
            default_response_class=ORJSONResponse,
            title=settings.TITLE,
            description=settings.DESCRIPTION,
            version=settings.version,
            docs_url=docs_url,
        )

        register_errors_handlers(app=self._api)

        if settings.IS_STATIC_DOCS and is_dev_mode:
            path = API_DEFAULT_ROOT_PATH + self._path
            register_static_docs(app=self._api, path=path)
