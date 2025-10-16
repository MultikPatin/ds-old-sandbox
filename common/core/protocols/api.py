from typing import Any, Protocol


class APIProtocol(Protocol):
    @property
    def api(self) -> Any: ...


class VersionedAPIProtocol(APIProtocol, Protocol):
    @property
    def path(self) -> str: ...
