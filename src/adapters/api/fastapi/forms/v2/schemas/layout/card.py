from common.fastapi.schemas import BsonIDSchema, OptionsSchema, TitleSchema


class LayoutCardTitle(TitleSchema):
    path: list[str]


class LayoutCardResponse(BsonIDSchema, OptionsSchema):
    rows: list[LayoutCardTitle]
