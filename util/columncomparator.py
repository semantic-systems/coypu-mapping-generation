from typing import List

from semanticlabeling.labeledcolumn import LabeledColumn


class IncomparableLabeledColumnException(Exception):
    """Thrown when two labeled columns of incomparable type are being compared"""


def get_closest_n(compare_column: LabeledColumn, other_columns: List[LabeledColumn], n) -> List[LabeledColumn]:
    def compare(column: LabeledColumn) -> float:
        try:
            diff = column - compare_column
        except IncomparableLabeledColumnException:
            diff = float('inf')

        return diff
    other_columns.sort(key=compare)

    return other_columns[:n]


def get_closest(compare_column: LabeledColumn, other_columns: List[LabeledColumn]) -> LabeledColumn | None:
    closest: LabeledColumn | None = None
    closest_diff: float = float('inf')

    for column in other_columns:
        try:
            diff = compare_column - column
        except IncomparableLabeledColumnException:
            continue

        if diff < closest_diff:
            closest_diff = diff
            closest = column

    return closest
