from beanie import Document, Link
from pydantic import Field
from pymongo import DESCENDING, IndexModel

from src.application.dtos.db.input import (
    InputBase,
    InputSingleBase,
    InputTableBase,
    InputTableChunkBase,
)
from src.application.dtos.db.layout import (
    LayoutBase,
    LayoutCardBase,
    LayoutSchemaBase,
    LayoutSingleBase,
    LayoutStyleBase,
    LayoutTableBase,
    LayoutValidationBase,
)

# INPUT PROPERTIES


class InputDocument(InputBase, Document):
    singles: list[Link["InputSingleDocument"]] | None = Field(default=None)
    tables: list[Link["InputTableDocument"]] | None = Field(default=None)
    layout: Link["LayoutDocument"]

    class Settings:
        name = "inputs"
        use_state_management = True
        max_nesting_depth = 1


# INPUT BLOCK PROPERTIES


class InputSingleDocument(InputSingleBase, Document):
    class Settings:
        name = "input_singles"
        max_nesting_depth = 0


class InputTableDocument(InputTableBase, Document):
    class Settings:
        name = "input_tables"
        max_nesting_depth = 0


class InputTableChunkDocument(InputTableChunkBase, Document):
    class Settings:
        name = "input_table_chunks"
        max_nesting_depth = 0


# LAYOUT PROPERTIES


class LayoutDocument(LayoutBase, Document):
    singles: list[Link["LayoutSingleDocument"]] | None = Field(default=None)
    tables: list[Link["LayoutTableDocument"]] | None = Field(default=None)
    card: Link["LayoutCardDocument"] | None = Field(default=None)

    class Settings:
        name = "layouts"
        use_state_management = True
        max_nesting_depth = 1
        indexes = [  # noqa: RUF012
            IndexModel(
                [
                    ("major_version", DESCENDING),
                    ("minor_version", DESCENDING),
                    ("key", DESCENDING),
                ],
                name="key_version_unique_idx_DESCENDING",
                unique=True,
            ),
        ]


# LAYOUT CARD PROPERTIES


class LayoutCardDocument(LayoutCardBase, Document):
    class Settings:
        name = "layout_cards"
        max_nesting_depth = 0


# LAYOUT BLOCK PROPERTIES


class LayoutSingleDocument(LayoutSingleBase, Document):
    class Settings:
        name = "layout_singles"
        max_nesting_depth = 0


class LayoutTableDocument(LayoutTableBase, Document):
    class Settings:
        name = "layout_tables"
        max_nesting_depth = 0


# LAYOUT CELL PROPERTIES


class LayoutCellDocument(LayoutSchemaBase, Document):
    class Settings:
        name = "layout_cell_schemas"
        max_nesting_depth = 0
        indexes = [  # noqa: RUF012
            IndexModel(
                [("hash", DESCENDING)],
                name="hash_idx_DESCENDING",
                unique=True,
            )
        ]


class LayoutValidationDocument(LayoutValidationBase, Document):
    class Settings:
        name = "layout_cell_validations"
        max_nesting_depth = 0
        indexes = [  # noqa: RUF012
            IndexModel(
                [("hash", DESCENDING)],
                name="hash_idx_DESCENDING",
                unique=True,
            )
        ]


class LayoutStyleDocument(LayoutStyleBase, Document):
    class Settings:
        name = "layout_cell_styles"
        max_nesting_depth = 0
        indexes = [  # noqa: RUF012
            IndexModel(
                [("hash", DESCENDING)],
                name="hash_idx_DESCENDING",
                unique=True,
            )
        ]
