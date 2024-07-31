from abc import ABC, abstractstaticmethod, abstractmethod
from types import NoneType
from typing import List, Dict, Set, Tuple, Union

import numpy as np
from pandas import Series, Timestamp

from semanticlabeling import ColumnType


class LabeledColumn(ABC):
    def __init__(self, column_name: str):
        self.column_name = column_name
        self.links: Dict[str, Set[LabeledColumn]] = {}

    def add_link_to_other_column(self, link_name: str, target_column: 'LabeledColumn'):
        if link_name not in self.links:
            self.links[link_name] = set()

        self.links[link_name].add(target_column)

    @staticmethod
    @abstractmethod
    def get_type() -> ColumnType:
        raise NotImplementedError()

    @abstractmethod
    def __sub__(self, other):
        raise NotImplementedError()


class IDColumn(LabeledColumn):
    def __init__(
            self,
            column_name: str,
            min_id_length: int,
            avg_id_length: float,
            max_id_length: int
    ):
        super().__init__(column_name)
        self.min_id_length = min_id_length
        self.avg_id_length = avg_id_length
        self.max_id_length = max_id_length

    @staticmethod
    def get_type() -> ColumnType:
        return ColumnType.ID

    def __str__(self):
        return f'IDColumn({self.column_name}, {self.min_id_length} < ' \
               f'[{self.avg_id_length:.4f}] < {self.max_id_length})'

    def __sub__(self, other):
        if not isinstance(other, IDColumn):
            from util.columncomparator import UncomparableException
            raise UncomparableException
        else:
            # TODO: re-check
            return abs(self.min_id_length - other.min_id_length) + \
                abs(self.avg_id_length - other.avg_id_length) + \
                abs(self.max_id_length - other.max_id_length)


class UntypedIDColumn(LabeledColumn):
    def __init__(self):
        super().__init__('untyped_id_column')
        self.entries: Set[str] = set()
        self.entry_links: Dict[str, Set[Tuple[str, LabeledColumn]]] = dict()

    def add_entry(self, id_str: str, links: Dict[str, LabeledColumn]):
        self.entries.add(id_str)
        entry_links = self.entry_links.get(id_str)

        if entry_links is None:
            entry_links = set()
            self.entry_links[id_str] = entry_links

        for link_name, target in links.items():
            entry_links.add((link_name, target))

    def contains_id(self, id_str: str) -> bool:
        return id_str in self.entries

    def get_id_links(self, id_str: str) -> Union[NoneType, Set[Tuple[str, LabeledColumn]]]:
        return self.entry_links.get(id_str)

    def remove_entry(self, id_str):
        self.entries.remove(id_str)
        self.entry_links.pop(id_str)

    @staticmethod
    def get_type() -> ColumnType:
        return ColumnType.ID

    def __sub__(self, other):
        # generally it makes no sense to compare even two UntypedIDColumn's as
        # they are just temporary containers for things that shall go into
        # something typed
        from util.columncomparator import UncomparableException
        raise UncomparableException()


class TypedIDColumn(IDColumn):
    def __init__(self, column_name: str, min_id_length: int, avg_id_length: float, max_id_length: int):
        super().__init__(column_name, min_id_length, avg_id_length, max_id_length)
        self._ids: Set[str] = set()
        self._id_cnt = 0

    def add_id(self, id_str: str):
        self._ids.add(id_str)
        self.min_id_length = min(self.min_id_length, len(id_str))
        self.max_id_length = max(self.max_id_length, len(id_str))

        self._id_cnt += 1
        id_len = len(id_str)
        self.avg_id_length = \
            (self.avg_id_length * (self._id_cnt - 1) / self._id_cnt) + \
            (id_len / self._id_cnt)

    def contains_id(self, id_str: str) -> bool:
        return id_str in self._ids


class TextColumn(LabeledColumn):
    def __init__(
            self,
            column_name: str,
            min_text_length: int,
            avg_text_length: float,
            max_text_length: int
    ):
        super().__init__(column_name)
        self.min_text_length = min_text_length
        self.avg_text_length = avg_text_length
        self.max_text_length = max_text_length
        self._values_cnt = 0

    def update_stats(self, text_length: int):
        self.min_text_length = min(self.min_text_length, text_length)
        self.max_text_length = max(self.max_text_length, text_length)

        self._values_cnt += 1
        self.avg_text_length = \
            (self.avg_text_length * (self._values_cnt - 1) / self._values_cnt) + \
            (text_length / self._values_cnt)

    @staticmethod
    def get_type() -> ColumnType:
        return ColumnType.Text

    def __str__(self):
        return f'TextColumn({self.column_name}, {self.min_text_length} < ' \
               f'[{self.avg_text_length:.4f}] < {self.max_text_length})'

    def __sub__(self, other):
        if not isinstance(other, TextColumn) and not isinstance(other, StringColumn):
            from util.columncomparator import UncomparableException
            raise UncomparableException()

        else:
            if isinstance(other, StringColumn):
                return abs(self.min_text_length - other.min_str_length) + \
                    abs(self.avg_text_length - other.avg_str_length) + \
                    abs(self.max_text_length - other.max_str_length)
            else:
                return abs(self.min_text_length - other.min_text_length) + \
                    abs(self.avg_text_length - other.avg_text_length) + \
                    abs(self.max_text_length - other.max_text_length)


class StringColumn(LabeledColumn):
    def __init__(
            self,
            column_name: str,
            min_str_length: int,
            avg_str_length: float,
            max_str_length: int
    ):
        super().__init__(column_name)
        self.min_str_length = min_str_length
        self.avg_str_length = avg_str_length
        self.max_str_length = max_str_length
        self._values_cnt = 0

    def update_stats(self, str_length: int):
        self.min_str_length = min(self.min_str_length, str_length)
        self.max_str_length = max(self.max_str_length, str_length)

        self._values_cnt += 1
        self.avg_str_length = \
            (self.avg_str_length * (self._values_cnt - 1) / self._values_cnt) + \
            (str_length / self._values_cnt)

    @staticmethod
    def get_type() -> ColumnType:
        return ColumnType.Str

    def __str__(self):
        return f'StringColumn({self.column_name}, {self.min_str_length} < ' \
               f'[{self.avg_str_length:.4f}] < {self.max_str_length})'

    def __sub__(self, other):
        if not isinstance(other, StringColumn) and not isinstance(other, TextColumn):
            from util.columncomparator import UncomparableException
            raise UncomparableException()

        if isinstance(other, TextColumn):
            return abs(self.min_str_length - other.min_text_length) + \
                abs(self.avg_str_length - other.avg_text_length) + \
                abs(self.max_str_length - other.max_text_length)
        else:
            return abs(self.min_str_length - other.min_str_length) + \
                abs(self.avg_str_length - other.avg_str_length) + \
                abs(self.max_str_length - other.max_str_length)


class BooleanColumn(LabeledColumn):
    def __init__(self, column_name: str, portion_true: float, portion_false: float):
        super().__init__(column_name)
        self.portion_true = portion_true
        self.portion_false = portion_false

    @staticmethod
    def get_type() -> ColumnType:
        return ColumnType.Boolean

    def __str__(self):
        return f'BooleanColumn({self.column_name}, {self.portion_true} True, ' \
               f'{self.portion_false} False)'

    def __sub__(self, other):
        if not isinstance(other, BooleanColumn):
            from util.columncomparator import UncomparableException
            raise UncomparableException()

        else:
            return abs(self.portion_true - other.portion_true) + \
                abs(self.portion_false - other.portion_false)


class CategoriesColumn(LabeledColumn):
    def __init__(self, column_name: str, categories: List[str]):
        super().__init__(column_name)
        self.categories = categories

    @staticmethod
    def get_type() -> ColumnType:
        return ColumnType.Categories

    def __str__(self):
        return f'CategoriesColumn({self.column_name}, [{" ".join(self.categories)}])'

    def __sub__(self, other):
        if not isinstance(other, CategoriesColumn):
            from util.columncomparator import UncomparableException
            raise UncomparableException

        else:
            return 1 - len(set(self.categories).intersection(set(other.categories))) / \
                len(set(self.categories).union(set(other.categories)))


class IntegerColumn(LabeledColumn):
    def __init__(
            self,
            column_name: str,
            min_value: int,
            avg_value: float,
            max_value: int,
            value_stddev: float
    ):
        super().__init__(column_name)
        self.min_value = min_value
        self.avg_value = avg_value
        self.max_value = max_value
        self.value_stddev = value_stddev

    @staticmethod
    def get_type() -> ColumnType:
        return ColumnType.Int

    def __str__(self):
        return f'IntegerColumn({self.column_name}, {self.min_value} < ' \
               f'[{self.avg_value:.4f} +/- {self.value_stddev:.4f}] < {self.max_value})'

    def __sub__(self, other):
        if not isinstance(other, IntegerColumn) and not isinstance(other, FloatColumn):
            from util.columncomparator import UncomparableException
            raise UncomparableException()

        else:
            return abs(self.min_value - other.min_value) + \
                abs(self.avg_value - other.avg_value) + \
                abs(self.max_value - other.max_value) + \
                abs(self.value_stddev - other.value_stddev)


class FloatColumn(LabeledColumn):
    def __init__(
            self,
            column_name: str,
            min_value: float,
            avg_value: float,
            max_value: float,
            value_stddev: float
    ):
        super().__init__(column_name)

        self.min_value = min_value
        self.avg_value = avg_value
        self.max_value = max_value
        self.value_stddev = value_stddev

    @staticmethod
    def get_type() -> ColumnType:
        return ColumnType.Float

    def __str__(self):
        return f'FloatColumn({self.column_name}, {self.min_value:.4f} < ' \
               f'[{self.avg_value:.4f} +/- {self.value_stddev:.4f}] < {self.max_value:.4f})'

    def __sub__(self, other):
        if not isinstance(other, FloatColumn) and not isinstance(other, IntegerColumn):
            from util.columncomparator import UncomparableException
            raise UncomparableException()
        else:
            return abs(self.min_value - other.min_value) + \
                abs(self.avg_value - other.avg_value) + \
                abs(self.max_value - other.max_value) + \
                abs(self.value_stddev - other.value_stddev)


class WGS84CoordinateColumn(FloatColumn):
    pass


class WGS84LatitudeColumn(WGS84CoordinateColumn):
    @staticmethod
    def looks_like_latitude_column(column: Series) -> bool:
        if np.min(column) > -90.0 and np.max(column) < 90.0 \
                and column.std() > 10:  # FIXME: threshold chosen arbitrarily
            return True
        else:
            return False

    @staticmethod
    def get_type() -> ColumnType:
        return ColumnType.Lat


class WGS84LongitudeColumn(WGS84CoordinateColumn):
    @staticmethod
    def looks_like_longitude_column(column: Series) -> bool:
        if np.min(column) > -180.0 and np.max(column) < 180.0 \
                and column.std() > 10:  # FIXME: threshold chosen arbitrarily
            return True
        else:
            return False

    @staticmethod
    def get_type() -> ColumnType:
        return ColumnType.Lon


class DateTimeColumn(LabeledColumn):
    def __init__(
            self,
            column_name: str,
            min_date_time: Timestamp,
            mean_date_time: Timestamp,
            max_date_time: Timestamp
    ):
        super().__init__(column_name)
        self.min_date_time = min_date_time
        self.mean_date_time = mean_date_time
        self.max_date_time = max_date_time

    @staticmethod
    def get_type() -> ColumnType:
        return ColumnType.DateTime

    def __str__(self):
        return f'DateTimeColumn({self.column_name}, {self.min_date_time} < ' \
               f'[{self.mean_date_time}] < {self.max_date_time})'

    def __sub__(self, other):
        if not isinstance(other, DateTimeColumn):
            from util.columncomparator import UncomparableException
            raise UncomparableException()

        else:
            return abs(self.min_date_time.timestamp() - other.min_date_time.timestamp()) + \
                abs(self.mean_date_time.timestamp() - other.mean_date_time.timestamp()) + \
                abs(self.max_date_time.timestamp() - other.max_date_time.timestamp())


class YetUnknownTypeColumn(LabeledColumn):
    def __init__(self, column_name: str):
        super().__init__(column_name)
        self.values = []

    def add_value(self, value):  # TODO: add type hint for value?
        self.values.append(value)

    @staticmethod
    def get_type() -> ColumnType:
        return ColumnType.Unknown

    def __sub__(self, other):
        # comparing unknown type columns to anything does not make sense
        from util.columncomparator import UncomparableException
        raise UncomparableException()