from common.core.dtos import HashDTO, IdDTO, LabelDTO, ValueDTO


class _ReferenceBase(LabelDTO, ValueDTO):
    pass


class ReferenceBase(HashDTO, _ReferenceBase):
    pass


class ReferenceCreate(_ReferenceBase):
    pass


class ReferenceDB(IdDTO, ReferenceBase):
    pass
