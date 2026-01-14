from abgroup_core.protocols import SessionProtocol

from src.application.protocols import LayoutTableRepositoryProtocol


class LayoutTableService:
    def __init__(
        self,
        repo: "LayoutTableRepositoryProtocol[SessionProtocol]",
    ) -> None:
        self._repo = repo
