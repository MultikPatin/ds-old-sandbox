from typing import TYPE_CHECKING

from src.application.dtos import (
    InputCreateValuesDTO,
    InputSingleCreateValuesDTO,
    InputTableCreateValuesDTO,
)

if TYPE_CHECKING:
    from src.application.dtos import (
        LayoutSingleWithLayersDTO,
        LayoutTableWithLayersDTO,
        LayoutWithBlockLayersDTO,
    )


def generate_template(
    layout: "LayoutWithBlockLayersDTO",
) -> InputCreateValuesDTO:
    singles = [_singles(s) for s in layout.singles] if layout.singles else None
    tables = [_tables(t) for t in layout.tables] if layout.tables else None
    return InputCreateValuesDTO(
        layout=layout.id,
        singles=singles,
        tables=tables,
    )


def _singles(item: "LayoutSingleWithLayersDTO") -> InputSingleCreateValuesDTO:
    if item.schemas is None:
        msg = "For generate template, schemas must be set in layout."
        raise ValueError(msg)

    keys = [s.key for s in item.schemas]
    kl = len(keys)

    values: list[str | None] = []
    if item.defaults is None:
        values.extend([None for _ in range(kl)])
    else:
        values.extend([d.value for d in item.defaults])

        vl = len(values)

        if vl > kl:
            msg = "incorrect number of defaults"
            raise ValueError(msg)
        if vl < kl:
            values.extend([None for _ in range(kl - vl)])

    return InputSingleCreateValuesDTO(
        key=item.key,
        values=dict(zip(keys, values, strict=False)),
    )


def _tables(
    item: "LayoutTableWithLayersDTO",
) -> InputTableCreateValuesDTO:
    if item.schemas is None:
        msg = "For generate template, schemas must be set in layout."
        raise ValueError(msg)

    number_of_columns = len(item.schemas[-1])

    if item.defaults is None:
        row = [None for _ in range(number_of_columns)]
        return InputTableCreateValuesDTO(key=item.key, values=[row])

    rows = []
    for defaults in item.defaults:
        values = [d.value for d in defaults]

        vl = len(values)

        if vl > number_of_columns:
            msg = "incorrect number of defaults"
            raise ValueError(msg)
        if vl < number_of_columns:
            values.extend([None for _ in range(number_of_columns - vl)])

        rows.append(values)

    return InputTableCreateValuesDTO(key=item.key, values=rows)
