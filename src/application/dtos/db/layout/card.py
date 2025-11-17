from common.core.dtos import IdDTO, OptionsDTO, TitleDTO


class LayoutCardTitle(TitleDTO):
    path: list[str]


# Update


class LayoutCardUpdateDTO(OptionsDTO):
    cells: list[LayoutCardTitle]


# Base


class LayoutCardBase(LayoutCardUpdateDTO):
    pass


class LayoutCardDB(IdDTO, LayoutCardBase):
    pass


# Create


class LayoutCardCreateDTO(LayoutCardBase):
    pass
