from abgroup_core.protocols import SessionProtocol

from src.application.protocols import LayoutSingleRepositoryProtocol


class LayoutSingleService:
    def __init__(
        self,
        repo: "LayoutSingleRepositoryProtocol[SessionProtocol]",
    ) -> None:
        self._repo = repo
