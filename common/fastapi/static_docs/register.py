from pathlib import Path
from typing import TYPE_CHECKING

from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

from common.core.enums import URLEnum

if TYPE_CHECKING:
    from fastapi import FastAPI
    from starlette.responses import HTMLResponse

_DIR = "static"

_SWAGGER_TITLE = "Swagger UI"
_SWAGGER_UI_SCRIPT_PATH = "/swagger-ui-bundle.js"
_SWAGGER_UI_STYLE_PATH = "/swagger-ui.css"


def register(*, app: "FastAPI", path: str) -> None:
    app.mount(
        URLEnum.static,
        StaticFiles(directory=Path(__file__).resolve().parent.joinpath(_DIR)),
        name=_DIR,
    )

    @app.get(URLEnum.docs, include_in_schema=False)
    async def custom_swagger_ui_html() -> "HTMLResponse":
        return get_swagger_ui_html(
            openapi_url=path + str(app.openapi_url),
            title=app.title + " - " + _SWAGGER_TITLE,
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=_DIR + _SWAGGER_UI_SCRIPT_PATH,
            swagger_css_url=_DIR + _SWAGGER_UI_STYLE_PATH,
        )

    @app.get(str(app.swagger_ui_oauth2_redirect_url), include_in_schema=False)
    async def swagger_ui_redirect() -> "HTMLResponse":
        return get_swagger_ui_oauth2_redirect_html()
