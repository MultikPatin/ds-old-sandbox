from common.fastapi.schemas import BsonIDSchema, LabelSchema, ValueSchema


class LayoutReferencesResponse(BsonIDSchema, ValueSchema, LabelSchema):
    pass
