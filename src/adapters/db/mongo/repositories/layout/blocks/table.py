from common.mongo import AddMixin, GetMixin

from src.application.dtos.db.layout import LayoutTableCreateDTO, LayoutTableDB


class LayoutTableRepository(
    GetMixin[LayoutTableDB],
    AddMixin[LayoutTableCreateDTO, LayoutTableDB],
):
    pass
