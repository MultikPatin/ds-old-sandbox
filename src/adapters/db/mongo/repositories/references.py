from common.mongo import AddMixin, GetMixin

from src.application.dtos.db.reference import ReferenceCreate, ReferenceDB


class ReferenceRepository(
    GetMixin[ReferenceDB],
    AddMixin[ReferenceCreate, ReferenceDB],
):
    pass
