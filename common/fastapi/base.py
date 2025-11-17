from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import APIRouter, FastAPI


class MBaseApp:
    _api: "FastAPI"

    @property
    def api(self) -> "FastAPI":
        return self._api


class VBaseApp(MBaseApp):
    _path: str

    @property
    def path(self) -> str:
        return self._path


class _BaseRouter:
    _router: "APIRouter"

    @property
    def router(self) -> "APIRouter":
        return self._router
