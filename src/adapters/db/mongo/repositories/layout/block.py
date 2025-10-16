from common.mongo import AddMixin, GetMixin

from src.application.dtos.db.layout import (
    LayoutSingleCreate,
    LayoutSingleDB,
    LayoutTableCreate,
    LayoutTableDB,
)


class LayoutSingleRepository(
    GetMixin[LayoutSingleDB],
    AddMixin[LayoutSingleCreate, LayoutSingleDB],
):
    pass


class LayoutTableRepository(
    GetMixin[LayoutTableDB],
    AddMixin[LayoutTableCreate, LayoutTableDB],
):
    pass
