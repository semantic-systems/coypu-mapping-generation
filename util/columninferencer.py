import numpy as np
import pandas as pd
from pandas._libs.tslibs.parsing import DateParseError

from semanticlabeling.labeledcolumn import YetUnknownTypeColumn, LabeledColumn, \
    WGS84LatitudeColumn, WGS84LongitudeColumn, FloatColumn, DateTimeColumn, \
    CategoriesColumn, TextColumn, BooleanColumn, IntegerColumn, IDColumn, \
    StringColumn


INTEGER_DENSITY_THRESHOLD = 0.9


def transform_column(
        unknown_type_column: YetUnknownTypeColumn,
        column_name: str
) -> LabeledColumn:

    series = pd.Series(unknown_type_column.values)

    return transform_series(series, column_name)


def transform_series(series: pd.Series, series_name: str) -> LabeledColumn:
    col_type = series.dtype

    # booleans
    if col_type == np.dtypes.BoolDType():
        return init_boolean_column(column_name=series_name, values=series)

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
        if _get_integer_density(series) > INTEGER_DENSITY_THRESHOLD and len(series.unique()) > 30:
            return init_id_column(column_name=series_name, values=series)

        else:
            return init_integer_column(column_name=series_name, values=series)

    # floats
    elif col_type in [
            np.dtypes.Float16DType(), np.dtypes.Float32DType(),
            np.dtypes.Float64DType(), np.dtypes.LongDoubleDType()]:
        return init_float_column(column_name=series_name, values=series)

    # complex numbers
    elif col_type in [
            np.dtypes.Complex64DType(), np.dtypes.Complex128DType(),
            np.dtypes.CLongDoubleDType()]:
        pass
        raise NotImplementedError()

    # strings
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
            date_time_series = pd.to_datetime(series, format='mixed')

        except (DateParseError, ValueError):
            # it is a string

            # TODO: Check for 'true'/'false' --> bool
            if series.map(lambda s: str(s).isnumeric()).all():
                try:
                    int_series = series.map(lambda s: int(s))

                    if _get_integer_density(int_series) > INTEGER_DENSITY_THRESHOLD:
                        return init_id_column(column_name=series_name, values=series)

                    else:
                        return init_integer_column(
                            column_name=series_name,
                            values=int_series
                        )

                except ValueError:
                    pass

            try:
                float_series = series.map(lambda s: float(s))

                return init_float_column(
                    column_name=series_name,
                    values=float_series
                )

            except ValueError:
                pass

            # Check the string lengths and how much they deviate. If the length
            # does not differ much we assume some kind of ID --> can be 'URI-fied'
            str_lengths: pd.Series = series.map(lambda s: len(s), na_action='ignore')

            if str_lengths.std() < 0.5:  # FIXME: value chosen arbitrarily
                # we assume some kind of ID
                return init_id_column(column_name=series_name, values=series)

            else:
                return init_str_column(column_name=series_name, values=series)

        else:
            # it is a date time series
            return init_date_time_column(column_name=series_name, series=date_time_series)


def init_float_column(column_name: str, values: pd.Series) -> LabeledColumn:
    col_min: float = float(np.min(values))
    col_avg: float = float(np.mean(values))
    col_max: float = float(np.max(values))
    col_stddev: float = values.std()

    if WGS84LatitudeColumn.looks_like_latitude_column(values) and \
            'lon' not in column_name:
        labeled_column = WGS84LatitudeColumn(
            column_name=column_name,
            min_value=col_min,
            avg_value=col_avg,
            max_value=col_max,
            value_stddev=col_stddev
        )

    elif WGS84LongitudeColumn.looks_like_longitude_column(values):
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

    return labeled_column


def init_date_time_column(column_name: str, series: pd.Series) -> LabeledColumn:
    col_min: pd.Timestamp = series.min()
    col_avg: pd.Timestamp = series.mean()
    col_max: pd.Timestamp = series.max()

    return DateTimeColumn(
        column_name=column_name,
        min_date_time=col_min,
        mean_date_time=col_avg,
        max_date_time=col_max
    )


def init_str_column(column_name: str, values: pd.Series) -> LabeledColumn:
    # TODO: Handle WSG strings like Point(1.23 42.11), Line( ), ...
    # Check if categorical values, i.e., the number of possible values is
    # small compared to the overall number of entries
    num_unique = values.nunique()
    num_all = sum(values.notnull())

    if (num_unique / num_all) < 0.1:  # FIXME: Value chosen arbitrarily
        # we assume categorical values, i.e. types --> can be 'URI-fied'

        return CategoriesColumn(
            column_name=column_name,
            categories=values.unique().tolist()
        )

    str_lengths = values.map(lambda t: len(t), na_action='ignore')

    # Check if there is any whitespace in the string values
    if values.map(lambda s: ' ' in s.strip(), na_action='ignore').any():

        return TextColumn(
            column_name=column_name,
            min_text_length=int(np.min(str_lengths)),
            avg_text_length=float(np.mean(str_lengths)),
            max_text_length=int(np.max(str_lengths))
        )

    else:
        return StringColumn(
            column_name=column_name,
            min_str_length=np.min(str_lengths),
            avg_str_length=float(np.mean(str_lengths)),
            max_str_length=np.max(str_lengths)
        )


def init_boolean_column(column_name: str, values: pd.Series) -> LabeledColumn:
    num_pos: int = sum(values == True)
    num_neg: int = sum(values == False)
    num_all: int = len(values)

    if num_all > 0:
        portion_true: float = num_pos / num_all
        portion_false: float = num_neg / num_all
    else:
        portion_true: float = 0.0
        portion_false: float = 0.0

    return BooleanColumn(
        column_name=column_name,
        portion_true=portion_true,
        portion_false=portion_false
    )


def init_integer_column(column_name: str, values: pd.Series) -> LabeledColumn:
    min_value: int = np.min(values)
    avg_value: float = float(np.mean(values))
    max_value: int = np.max(values)
    value_stddev: float = float(np.std(values))

    return IntegerColumn(
        column_name=column_name,
        min_value=min_value,
        avg_value=avg_value,
        max_value=max_value,
        value_stddev=value_stddev
    )


def init_id_column(column_name: str, values: pd.Series):
    str_lengths = values.map(lambda x: len(str(x)), na_action='ignore')
    min_id_len: int = np.min(str_lengths)
    max_id_len: int = np.max(str_lengths)
    avg_id_len: float = float(np.mean(str_lengths))

    return IDColumn(
        column_name=column_name,
        min_id_length=min_id_len,
        avg_id_length=avg_id_len,
        max_id_length=max_id_len
    )


def _get_integer_density(series: pd.Series) -> float:
    """
    'Integer density' here reflects how densely the data range of the input
    series is packed. If we assume a series of integers

        1, 2, 3, 4, 5, 6, 7, 8, 9, 10

    we have a data range of 10 (from 1 to 10) and exactly 10 unique entries
    which amounts to a perfect density of 1. This number would, e.g., suggest
    that the numbers reflect some kind of ID.

    If we have an integer series of

        2001, 1982, 1990, 2000, 1999, 2000, 2003, 1999, 2001, 1992

    the data range would be 21 (from 1982 to 2003) with 7 unique entries. This
    time the density for the range would be 0.3333.
    """
    min_int = np.min(series)
    max_int = np.max(series)
    range_ = max_int - min_int

    if range_:
        return len(series.unique()) / range_

    else:
        return 0.0
