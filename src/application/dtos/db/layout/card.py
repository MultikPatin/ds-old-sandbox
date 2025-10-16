from common.core.dtos import IdDTO, OptionsDTO, TitleDTO


class LayoutCardTitle(TitleDTO):
    path: list[str]


class LayoutCardBase(OptionsDTO):
    rows: list[LayoutCardTitle]


class LayoutCardCreate(LayoutCardBase):
    pass


class LayoutCardDB(IdDTO, LayoutCardBase):
    pass
