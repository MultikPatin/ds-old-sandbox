from fastapi import APIRouter, FastAPI


class _App:
    _api: FastAPI

    @staticmethod
    def _check_path(path: str) -> None:
        if not path.startswith("/"):
            msg = f"Path should start with slash (/), but got {path!r} instead."
            raise ValueError(msg)

    @property
    def api(self) -> FastAPI:
        return self._api


class _VersionedApp(_App):
    _path: str

    @property
    def path(self) -> str:
        return self._path


class _BaseRouter:
    _router: APIRouter

    @property
    def router(self) -> APIRouter:
        return self._router
