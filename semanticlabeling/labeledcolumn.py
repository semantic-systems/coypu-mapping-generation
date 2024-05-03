from abc import ABC
from typing import List

import numpy as np
from pandas import Series, Timestamp


class LabeledColumn(ABC):
    def __init__(self, column_name: str):
        self.column_name = column_name
        self.links = {}

    def add_link_to_other_column(self, link_name: str, target_column: 'LabeledColumn'):
        if link_name not in self.links:
            self.links[link_name] = []

        self.links[link_name].append(target_column)


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


class CategoriesColumn(LabeledColumn):
    def __init__(self, column_name: str, categories: List[str]):
        super().__init__(column_name)
        self.categories = categories


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


class WGS84LongitudeColumn(WGS84CoordinateColumn):
    @staticmethod
    def looks_like_longitude_column(column: Series) -> bool:
        if np.min(column) > -180.0 and np.max(column) < 180.0 \
                and column.std() > 10:  # FIXME: threshold chosen arbitrarily
            return True
        else:
            return False


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
