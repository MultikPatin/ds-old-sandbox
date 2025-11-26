from common.mongo import AddMixin, GetMixin

from src.application.dtos.db.layout import LayoutSingleCreateDTO, LayoutSingleDB


class LayoutSingleRepository(
    GetMixin[LayoutSingleDB],
    AddMixin[LayoutSingleCreateDTO, LayoutSingleDB],
):
    pass
