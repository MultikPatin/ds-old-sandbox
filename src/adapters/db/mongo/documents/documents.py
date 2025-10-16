from beanie import BackLink, Document, Link, UnionDoc
from pydantic import Field
from pymongo import ASCENDING, DESCENDING, IndexModel

from src.application.dtos.db.input import (
    InputBase,
    InputSingleBase,
    InputTableBase,
    InputTableChunkBase,
)
from src.application.dtos.db.key import KeyBase
from src.application.dtos.db.layout import (
    LayoutBase,
    LayoutCardBase,
    LayoutHeaderCellBase,
    LayoutRequiredCellBase,
    LayoutRequiredRowBase,
    LayoutSingleBase,
    LayoutStyleBase,
    LayoutTableBase,
    LayoutTooltipBase,
    LayoutValidationBase,
)
from src.application.dtos.db.model import ModelBase
from src.application.dtos.db.reference import ReferenceBase

# INPUT PROPERTIES -------------------


class InputsDocument(InputBase, Document):
    layout: Link["LayoutsDocument"]

    singles: list[Link["InputSinglesDocument"]] | None = Field(default=None)
    tables: list[Link["InputTableDocument"]] | None = Field(default=None)

    class Settings:
        name = "inputs"
        use_state_management = True
        indexes = [  # noqa: RUF012
            IndexModel(
                [("created", DESCENDING)],
                name="created_idx_DESCENDING",
            ),
            IndexModel(
                [("updated", DESCENDING)],
                name="updated_idx_DESCENDING",
            ),
        ]


class InputSinglesDocument(InputSingleBase, Document):
    class Settings:
        name = "input_singles"
        use_state_management = True
        max_nesting_depth = 0


class InputTableDocument(InputTableBase, Document):
    chunks: list[Link["InputTablesChunksDocument"]]

    class Settings:
        name = "input_tables"
        use_state_management = True
        max_nesting_depth = 1


class InputTablesChunksDocument(InputTableChunkBase, Document):
    class Settings:
        name = "input_table_chunks"
        use_state_management = True
        max_nesting_depth = 0


# MODEL PROPERTIES -------------------


class ModelsDocument(ModelBase, Document):
    keys: list[BackLink["KeysDocument"]] = Field(
        json_schema_extra={"original_field": "model"}
    )

    class Settings:
        name = "models"
        use_state_management = True
        indexes = [  # noqa: RUF012
            IndexModel(
                [("created", DESCENDING)],
                name="created_idx_DESCENDING",
            ),
            IndexModel(
                [("updated", DESCENDING)],
                name="updated_idx_DESCENDING",
            ),
            IndexModel(
                [
                    ("title", ASCENDING),
                    ("major_version", ASCENDING),
                    ("minor_version", ASCENDING),
                ],
                name="title_version_idx_ASCENDING",
                unique=True,
            ),
        ]


# KEY PROPERTIES -------------------


class KeysDocument(KeyBase, Document):
    model: Link["ModelsDocument"]
    layout: Link["LayoutsDocument"]

    class Settings:
        name = "keys"
        indexes = [  # noqa: RUF012
            IndexModel(
                [("model", ASCENDING), ("layout", ASCENDING)],
                name="model_layout_idx_ASCENDING",
                unique=True,
            )
        ]


# LAYOUT OTHER PROPERTIES -------------------


class ReferencesDocument(ReferenceBase, Document):
    class Settings:
        name = "references"
        max_nesting_depth = 0
        indexes = [  # noqa: RUF012
            IndexModel(
                [("hash", DESCENDING)],
                name="hash_idx_DESCENDING",
                unique=True,
            )
        ]


# LAYOUT PROPERTIES -------------------


class ParentLayout(UnionDoc):
    class Settings:
        name = "layouts_union"
        class_id = "_class_id"


class LayoutsDocument(LayoutBase, Document):
    card: Link["LayoutCardsDocument"] | None = Field(default=None)

    singles: list[Link["LayoutSinglesDocument"]] | None = Field(default=None)
    tables: list[Link["LayoutTablesDocument"]] | None = Field(default=None)

    class Settings:
        name = "layout"
        use_state_management = True
        union_doc = ParentLayout
        max_nesting_depth = 4
        indexes = [  # noqa: RUF012
            IndexModel(
                [("created", DESCENDING)],
                name="created_idx_DESCENDING",
            ),
            IndexModel(
                [("updated", DESCENDING)],
                name="updated_idx_DESCENDING",
            ),
        ]


class LayoutCardsDocument(LayoutCardBase, Document):
    class Settings:
        name = "card"
        union_doc = ParentLayout
        max_nesting_depth = 0


# LAYOUT BLOCK PROPERTIES -------------------


class ParentLayoutBlocks(UnionDoc):
    class Settings:
        name = "layout_blocks_union"
        class_id = "_class_id"


class LayoutSinglesDocument(LayoutSingleBase, Document):
    cells: list[Link["LayoutHeaderCellsDocument"]] | None = Field(default=None)

    class Settings:
        name = "single"
        union_doc = ParentLayoutBlocks
        use_state_management = True
        max_nesting_depth = 2


class LayoutTablesDocument(LayoutTableBase, Document):
    headers: list[Link["LayoutHeaderCellsDocument"]]
    rows: list[Link["LayoutRequiredRowsDocument"]] | None = Field(default=None)

    class Settings:
        name = "table"
        union_doc = ParentLayoutBlocks
        use_state_management = True
        max_nesting_depth = 3


# LAYOUT CELL PROPERTIES -------------------


class ParentLayoutCells(UnionDoc):
    class Settings:
        name = "layout_cells_union"
        class_id = "_class_id"
        indexes = [  # noqa: RUF012
            IndexModel(
                [("hash", DESCENDING)],
                name="hash_idx_DESCENDING",
                unique=True,
            )
        ]


class LayoutRequiredRowsDocument(LayoutRequiredRowBase, Document):
    cells: list[Link["LayoutRequiredCellsDocument"]] | None = Field(
        default=None
    )

    class Settings:
        name = "row_required"
        union_doc = ParentLayoutCells
        use_state_management = True
        max_nesting_depth = 2


class LayoutRequiredCellsDocument(LayoutRequiredCellBase, Document):
    tooltip: Link["LayoutTooltipsDocument"] | None = Field(default=None)

    class Settings:
        name = "cell_required"
        union_doc = ParentLayoutCells
        max_nesting_depth = 1


class LayoutHeaderCellsDocument(LayoutHeaderCellBase, Document):
    validation: Link["LayoutValidationsDocument"] | None = Field(default=None)
    style: Link["LayoutStylesDocument"] | None = Field(default=None)
    tooltip: Link["LayoutTooltipsDocument"] | None = Field(default=None)
    references: list[Link["ReferencesDocument"]] | None = Field(default=None)

    class Settings:
        name = "cell_header"
        union_doc = ParentLayoutCells
        max_nesting_depth = 1


class LayoutTooltipsDocument(LayoutTooltipBase, Document):
    class Settings:
        name = "tooltip"
        union_doc = ParentLayoutCells
        max_nesting_depth = 0


class LayoutStylesDocument(LayoutStyleBase, Document):
    class Settings:
        name = "style"
        union_doc = ParentLayoutCells
        max_nesting_depth = 0


class LayoutValidationsDocument(LayoutValidationBase, Document):
    class Settings:
        name = "validation"
        union_doc = ParentLayoutCells
        max_nesting_depth = 0
