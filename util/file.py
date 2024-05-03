import random
import subprocess
from abc import ABC, abstractmethod
from typing import Tuple, List

import pandas as pd
import numpy as np
from pandas import Series, Timestamp
from pandas._libs.tslibs.parsing import DateParseError

from semanticlabeling.labeledcolumn import IDColumn, TextColumn, LabeledColumn,\
    CategoriesColumn, WGS84LatitudeColumn, WGS84LongitudeColumn, FloatColumn, \
    DateTimeColumn
from semanticlabeling import ColumnType


class InputFile(ABC):
    columns: List[LabeledColumn]

    def __init__(self, input_file_path: str, has_header: bool = False):
        self.input_file_path = input_file_path
        self.has_header = has_header

    @abstractmethod
    def get_column_keys(self):
        pass

    @abstractmethod
    def get_column_type(self, column_id: str) -> ColumnType:
        pass

    @abstractmethod
    def get_numeric_range(self, column_id: str) -> Tuple[float, float]:
        pass

    @abstractmethod
    def get_avg(self, column_id: str) -> float:
        pass

    @staticmethod
    def get_file_type_by_str(file_format_str: str):
        file_format_str = file_format_str.lower()

        if file_format_str == 'csv':
            return CSVInputFile

        elif file_format_str == 'sampled_csv':
            return SampledCSVInputFile

        else:
            raise RuntimeError(f'Unknown file format: {file_format_str}')


class CSVInputFile(InputFile):
    def get_column_keys(self):
        raise NotImplementedError()

    def get_column_type(self, column_id: str) -> ColumnType:
        raise NotImplementedError()

    def get_numeric_range(self, column_id: str) -> Tuple[float, float]:
        raise NotImplementedError()

    def get_avg(self, column_id: str) -> float:
        raise NotImplementedError()


class SampledCSVInputFile(CSVInputFile):
    def __init__(
            self,
            input_file_path: str,
            has_header: bool = False,
            max_rows: int = 10000
    ):
        self.columns: List[LabeledColumn] = []

        wc_out = subprocess.check_output(['wc', '-l', input_file_path])
        num_lines = int(wc_out.strip().split(b' ')[0])

        if num_lines > max_rows:
            drop_probability = max_rows / num_lines

            df = pd.read_csv(
                filepath_or_buffer=input_file_path,
                skiprows=lambda i: i > 0 and random.random() > drop_probability,
            )

        else:
            df = pd.read_csv(
                filepath_or_buffer=input_file_path,
            )

        is_first_column = True
        for column in df.columns:
            series = df[column]

            if is_first_column:
                # we assume the first column in a CSV fil is always an ID column
                self._init_id_colum(column, series)
                is_first_column = False
                continue

            col_type = series.dtype
            if col_type == np.dtypes.BoolDType():
                pass
                raise NotImplementedError()

            # integers
            elif col_type in [
                    np.dtypes.Int8DType(), np.dtypes.UInt8DType(),
                    np.dtypes.Int16DType(), np.dtypes.UInt16DType(),
                    np.dtypes.Int32DType(), np.dtypes.UInt32DType(),
                    np.dtypes.Int64DType(), np.dtypes.UInt64DType(),
                    np.dtypes.ByteDType(), np.dtypes.UByteDType(),
                    np.dtypes.ShortDType(), np.dtypes.UShortDType(),
                    np.dtypes.IntDType(), np.dtypes.UIntDType(),
                    np.dtypes.LongDType(), np.dtypes.ULongDType(),
                    np.dtypes.LongLongDType(), np.dtypes.ULongLongDType()]:
                pass
                raise NotImplementedError()

            # floats
            elif col_type in [
                    np.dtypes.Float16DType(), np.dtypes.Float32DType(),
                    np.dtypes.Float64DType(), np.dtypes.LongDoubleDType()]:
                self._init_float_column(column_name=column, column=series)

            # complex numbers
            elif col_type in [
                    np.dtypes.Complex64DType(), np.dtypes.Complex128DType(),
                    np.dtypes.CLongDoubleDType()]:
                pass
                raise NotImplementedError()

            # # strings
            # elif col_type in [np.dtypes.BytesDType(), np.dtypes.BytesDType()]:
            #     pass
            #     raise NotImplementedError()

            # # time formats
            # elif col_type in [
            #         np.dtypes.DateTime64DType(), np.dtypes.TimeDelta64DType()]:
            #     pass
            #     raise NotImplementedError()

            # strings or dates
            else:
                # check for date first
                try:
                    date_time_series = pd.to_datetime(series)
                except DateParseError:
                    # it is a string
                    self._init_str_column(column_name=column, column=series)
                    continue

                else:
                    # it is a date time series
                    self._init_date_time_column(column, date_time_series)

    def _init_date_time_column(self, column_name: str, column: Series):
        col_min: Timestamp = column.min()
        col_avg = column.mean()
        col_max = column.max()

        labeled_column = DateTimeColumn(
            column_name=column_name,
            min_date_time=col_min,
            mean_date_time=col_avg,
            max_date_time=col_max
        )

        self.columns.append(labeled_column)
        # add link to main ID column (assumed to be the first one in
        # self.columns
        self.columns[0].add_link_to_other_column(column_name, labeled_column)

    def _init_str_column(self, column_name: str, column: Series):
        # Check if categorical values, i.e., the number of possible values is
        # small compared to the overall number of entries
        num_unique = column.nunique()
        num_all = sum(column.notnull())
        if (num_unique / num_all) < 0.1:  # FIXME: Value chosen arbitrarily
            # we assume categorical values, i.e. types --> can be 'URI-fied'
            labeled_column = CategoriesColumn(
                column_name=column_name,
                categories=column.unique().tolist()
            )

            self.columns.append(labeled_column)
            # add link to main ID column (assumed to be the first on ein
            # self.columns
            self.columns[0].add_link_to_other_column(column_name, labeled_column)

            return

        # Check if there is any whitespace in the string values
        if column.map(lambda s: ' ' in s.strip(), na_action='ignore').any():
            text_lengths = column.map(lambda t: len(t), na_action='ignore')
            labeled_column = TextColumn(
                    column_name=column_name,
                    min_text_length=int(np.min(text_lengths)),
                    avg_text_length=float(np.mean(text_lengths)),
                    max_text_length=int(np.max(text_lengths))
            )

            self.columns.append(labeled_column)
            # add link to main ID column (assumed to be the first on ein
            # self.columns
            self.columns[0].add_link_to_other_column(column_name, labeled_column)

            return

        # Check the string lengths and how much they deviate. If the length
        # does not differ much we assume some kind of ID --> can be 'URI-fied'
        str_lengths: Series = column.map(lambda s: len(s), na_action='ignore')
        if str_lengths.std() < 0.5:  # FIXME: value chosen arbitrarily
            # we assume some kind of ID
            pass
            raise NotImplementedError()
        pass
        raise NotImplementedError()

    def _init_id_colum(self, column_name: str, column: Series):
        if column.dtype in [
                np.dtypes.Int8DType(), np.dtypes.UInt8DType(),
                np.dtypes.Int16DType(), np.dtypes.UInt16DType(),
                np.dtypes.Int32DType(), np.dtypes.UInt32DType(),
                np.dtypes.Int64DType(), np.dtypes.UInt64DType(),
                np.dtypes.ByteDType(), np.dtypes.UByteDType(),
                np.dtypes.ShortDType(), np.dtypes.UShortDType(),
                np.dtypes.IntDType(), np.dtypes.UIntDType(),
                np.dtypes.LongDType(), np.dtypes.ULongDType(),
                np.dtypes.LongLongDType(), np.dtypes.ULongLongDType()]:
            id_lengths = column.map(lambda i: len(str(i)))
        else:
            id_lengths = column.map(lambda s: len(s))

        self.columns.append(
            IDColumn(
                column_name=column_name,
                min_id_length=int(np.min(id_lengths)),
                avg_id_length=float(np.average(id_lengths)),
                max_id_length=int(np.max(id_lengths))
            )
        )

    def _init_float_column(self, column_name: str, column: Series):
        col_min = float(np.min(column))
        col_avg = float(np.mean(column))
        col_max = float(np.max(column))
        col_stddev = column.std()

        if WGS84LatitudeColumn.looks_like_latitude_column(column) and \
                'lon' not in column_name:
            labeled_column = WGS84LatitudeColumn(
                column_name=column_name,
                min_value=col_min,
                avg_value=col_avg,
                max_value=col_max,
                value_stddev=col_stddev
            )

        elif WGS84LongitudeColumn.looks_like_longitude_column(column):
            labeled_column = WGS84LongitudeColumn(
                column_name=column_name,
                min_value=col_min,
                avg_value=col_avg,
                max_value=col_max,
                value_stddev=col_stddev
            )

        else:
            labeled_column = FloatColumn(
                column_name=column_name,
                min_value=col_min,
                avg_value=col_avg,
                max_value=col_max,
                value_stddev=col_stddev
            )

        self.columns.append(labeled_column)
        # add link to main ID column (assumed to be the first on ein
        # self.columns
        self.columns[0].add_link_to_other_column(column_name, labeled_column)
