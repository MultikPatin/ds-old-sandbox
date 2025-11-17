from typing import Any, Protocol


class MAppProtocol(Protocol):
    @property
    def api(self) -> Any: ...


class VAppProtocol(MAppProtocol, Protocol):
    @property
    def path(self) -> str: ...
