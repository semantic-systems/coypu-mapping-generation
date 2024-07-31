from typing import List

from semanticlabeling.labeledcolumn import LabeledColumn


class UncomparableException(Exception):
    """Thrown when two labeled columns of uncomparable type are being compared"""


def get_closest(compare_column: LabeledColumn, other_columns: List[LabeledColumn]) -> LabeledColumn:
    raise NotImplementedError()
