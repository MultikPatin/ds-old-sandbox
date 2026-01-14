from abgroup_core.protocols import SessionProtocol

from src.application.protocols import LayoutCardRepositoryProtocol


class LayoutCardService:
    def __init__(
        self,
        repo: "LayoutCardRepositoryProtocol[SessionProtocol]",
    ) -> None:
        self._repo = repo
