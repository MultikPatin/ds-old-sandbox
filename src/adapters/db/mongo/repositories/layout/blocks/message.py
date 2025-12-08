from common.mongo import AddMixin, GetMixin

from src.application.dtos.db.layout import (
    LayoutMessageCreateDTO,
    LayoutMessageDB,
)


class LayoutMessageRepository(
    GetMixin[LayoutMessageDB],
    AddMixin[LayoutMessageCreateDTO, LayoutMessageDB],
):
    pass
