from common.mongo import AddMixin, GetMixin

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


class LayoutRequiredRowRepository(
    GetMixin[LayoutRequiredRowFullLInks],
    AddMixin[LayoutRequiredRowCreate, LayoutRequiredRowFullLInks],
):
    pass


class LayoutRequiredCellRepository(
    GetMixin[LayoutRequiredCellFullLinks],
    AddMixin[LayoutRequiredCellCreate, LayoutRequiredCellFullLinks],
):
    pass


class LayoutHeaderCellRepository(
    GetMixin[LayoutHeaderCellDB],
    AddMixin[LayoutHeaderCellCreate, LayoutHeaderCellDB],
):
    pass


class LayoutTooltipRepository(
    GetMixin[LayoutTooltipDB],
    AddMixin[LayoutTooltipCreate, LayoutTooltipDB],
):
    pass


class LayoutStyleRepository(
    GetMixin[LayoutStyleDB],
    AddMixin[LayoutStyleCreate, LayoutStyleDB],
):
    pass


class LayoutValidationRepository(
    GetMixin[LayoutValidationDB],
    AddMixin[LayoutValidationCreate, LayoutValidationDB],
):
    pass
