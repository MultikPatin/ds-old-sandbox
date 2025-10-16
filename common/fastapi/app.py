from typing import TypeVar

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
from common.core.protocols import VersionedAPIProtocol

from .base import _App, _VersionedApp
from .errors_handlers import register_errors_handlers
from .middlewares import ProcessTimeHeaderMiddleware
from .settings import MainAPISettings, VersionedAPISettings
from .static import register_static_docs_routes

_MainSettings = TypeVar("_MainSettings", bound=MainAPISettings)
_VersionedAPISettings = TypeVar(
    "_VersionedAPISettings", bound=VersionedAPISettings
)


class App(_App):
    def __init__(
        self,
        settings: _MainSettings,
        lifespan: Lifespan[FastAPI] | None = None,
    ):
        self._check_path(API_DEFAULT_ROOT_PATH)

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

    def mount(self, app: VersionedAPIProtocol) -> None:
        self._api.mount(app.path, app.api)


class VersionedApp(_VersionedApp):
    def __init__(
        self,
        is_dev_mode: bool,
        settings: _VersionedAPISettings,
    ) -> None:
        self._check_path(settings.PATH)
        self._path = settings.PATH

        docs_url = (
            None if settings.IS_STATIC_DOCS or not is_dev_mode else URLEnum.docs
        )

        self._api = FastAPI(
            default_response_class=ORJSONResponse,
            title=settings.TITLE,
            description=settings.DESCRIPTION,
            version=settings.VERSION,
            docs_url=docs_url,
        )

        register_errors_handlers(app=self._api)

        if settings.IS_STATIC_DOCS and is_dev_mode:
            register_static_docs_routes(
                app=self._api,
                path=API_DEFAULT_ROOT_PATH + self._path,
            )
