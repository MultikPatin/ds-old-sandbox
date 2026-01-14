from typing import Protocol

from abgroup_core.protocols import SessionProtocol

from src.application.dtos.db import (
    LayoutSingleCreateDTO,
    LayoutSingleDB,
)

from ._base import _RepositoryProtocol


class LayoutSingleRepositoryProtocol[Session: SessionProtocol](
    _RepositoryProtocol[
        LayoutSingleDB,
        LayoutSingleCreateDTO,
        Session,
    ],
    Protocol,
): ...
