from typing import Protocol

from common.core.protocols import AdderProtocol, GetterProtocol, SessionProtocol

from src.application.dtos.db.layout import (
    LayoutHeaderCellCreate,
    LayoutHeaderCellDB,
    LayoutRequiredCellCreate,
    LayoutRequiredCellFullLinks,
    LayoutRequiredRowCreate,
    LayoutRequiredRowFullLInks,
    LayoutStyleCreate,
    LayoutStyleDB,
    LayoutTooltipCreate,
    LayoutTooltipDB,
    LayoutValidationCreate,
    LayoutValidationDB,
)


class LayoutRequiredRowRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[LayoutRequiredRowFullLInks, Session],
    AdderProtocol[LayoutRequiredRowCreate, LayoutRequiredRowFullLInks, Session],
    Protocol,
): ...


class LayoutRequiredCellRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[LayoutRequiredCellFullLinks, Session],
    AdderProtocol[
        LayoutRequiredCellCreate, LayoutRequiredCellFullLinks, Session
    ],
    Protocol,
): ...


class LayoutHeaderCellRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[LayoutHeaderCellDB, Session],
    AdderProtocol[LayoutHeaderCellCreate, LayoutHeaderCellDB, Session],
    Protocol,
): ...


class LayoutTooltipRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[LayoutTooltipDB, Session],
    AdderProtocol[LayoutTooltipCreate, LayoutTooltipDB, Session],
    Protocol,
): ...


class LayoutStyleRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[LayoutStyleDB, Session],
    AdderProtocol[LayoutStyleCreate, LayoutStyleDB, Session],
    Protocol,
): ...


class LayoutValidationRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[LayoutValidationDB, Session],
    AdderProtocol[LayoutValidationCreate, LayoutValidationDB, Session],
    Protocol,
): ...
