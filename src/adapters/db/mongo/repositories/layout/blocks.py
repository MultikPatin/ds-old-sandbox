from common.mongo import AddMixin, GetMixin

from src.application.dtos.db.layout import (
    LayoutSingleCreateDTO,
    LayoutSingleDB,
    LayoutTableCreateDTO,
    LayoutTableDB,
)


class LayoutSingleRepository(
    GetMixin[LayoutSingleDB],
    AddMixin[LayoutSingleCreateDTO, LayoutSingleDB],
):
    pass


class LayoutTableRepository(
    GetMixin[LayoutTableDB],
    AddMixin[LayoutTableCreateDTO, LayoutTableDB],
):
    pass
