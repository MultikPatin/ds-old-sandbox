from common.core.dtos import IdDTO, KeyDTO

from .cells import LayoutHeaderCellCreate, LayoutHeaderCellFullLinks


class LayoutSingleBase(KeyDTO):
    pass


class LayoutSingleCreate(KeyDTO):
    cells: list[LayoutHeaderCellCreate]


class LayoutSingleDB(IdDTO, LayoutSingleBase):
    pass


class LayoutSingleFullLinks(LayoutSingleDB):
    cells: list[LayoutHeaderCellFullLinks]
