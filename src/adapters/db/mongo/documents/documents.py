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
    LayoutDefaultBase,
    LayoutMessageBase,
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
    card: Link["LayoutCardDocument"] | None = Field(default=None)

    singles: list[Link["LayoutSingleDocument"]] | None = Field(default=None)
    tables: list[Link["LayoutTableDocument"]] | None = Field(default=None)
    messages: list[Link["LayoutMessageDocument"]] | None = Field(default=None)

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


# LAYOUT BLOCK PROPERTIES


class LayoutCardDocument(LayoutCardBase, Document):
    class Settings:
        name = "layout_block_cards"
        max_nesting_depth = 0


class LayoutSingleDocument(LayoutSingleBase, Document):
    class Settings:
        name = "layout_block_singles"
        max_nesting_depth = 0


class LayoutTableDocument(LayoutTableBase, Document):
    class Settings:
        name = "layout_block_tables"
        max_nesting_depth = 0


class LayoutMessageDocument(LayoutMessageBase, Document):
    class Settings:
        name = "layout_block_messages"
        max_nesting_depth = 0


# LAYOUT CELL PROPERTIES


class LayoutSchemaDocument(LayoutSchemaBase, Document):
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


class LayoutDefaultDocument(LayoutDefaultBase, Document):
    class Settings:
        name = "layout_cell_defaults"
        max_nesting_depth = 0
        indexes = [  # noqa: RUF012
            IndexModel(
                [("hash", DESCENDING)],
                name="hash_idx_DESCENDING",
                unique=True,
            )
        ]
