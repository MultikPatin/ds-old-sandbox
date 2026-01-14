from typing import Protocol

from abgroup_core.protocols import SessionProtocol

from src.application.dtos.db import LayoutTableCreateDTO, LayoutTableDB

from ._base import _RepositoryProtocol


class LayoutTableRepositoryProtocol[Session: SessionProtocol](
    _RepositoryProtocol[
        LayoutTableDB,
        LayoutTableCreateDTO,
        Session,
    ],
    Protocol,
): ...
