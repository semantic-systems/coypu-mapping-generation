import random
import subprocess
from abc import ABC, abstractmethod
from typing import Tuple, List

import pandas as pd

from semanticlabeling.labeledcolumn import LabeledColumn
from semanticlabeling import ColumnType
from util import columninferencer


class InputFile(ABC):
    columns: List[LabeledColumn]

    def __init__(self, input_file_path: str, has_header: bool = False):
        self.input_file_path = input_file_path
        self.has_header = has_header

    @abstractmethod
    def get_column_keys(self) -> List[str]:
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

    def __init__(self, input_file_path: str, has_header: bool = False):
        super().__init__(input_file_path, has_header)
        self.columns = []

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
        super().__init__(input_file_path, has_header)
        self.columns: List[LabeledColumn] = []

        # FIXME: Assumes Unix
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
        for column_name in df.columns:
            series = df[column_name]

            if is_first_column:
                # we assume the first column in a CSV fil is always an ID column
                id_column = columninferencer.init_id_column(column_name, series)
                self.columns.append(id_column)
                is_first_column = False
                continue

            labeled_column = columninferencer.transform_series(
                series=series,
                series_name=column_name
            )

            self.columns[0].add_link_to_other_column(column_name, labeled_column)
            self.columns.append(labeled_column)

    def get_column_keys(self):
        return [column.column_name for column in self.columns]

    def get_column_type(self, column_id: str) -> ColumnType:
        desired_column = None
        for column in self.columns:
            if column.column_name == column_id:
                desired_column = column
                break

        if desired_column is None:
            return ColumnType.Unknown
        else:
            return desired_column.get_type()

    # FIXME: Is this needed?
    def get_numeric_range(self, column_id: str) -> Tuple[float, float]:
        raise NotImplementedError()

    # FIXME: Is this needed?
    def get_avg(self, column_id: str) -> float:
        raise NotImplementedError()
