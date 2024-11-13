from datetime import time

import numpy as np
from pandas import Timestamp, Series
from rdflib import Literal, URIRef, XSD

import pandas as pd

from semanticlabeling.labeledcolumn import IntegerColumn, StringColumn, \
    TextColumn, LabeledColumn, FloatColumn, DateTimeColumn, BooleanColumn, \
    TypedIDColumn
from util.type import TypeHandler

import logging

logger = logging.getLogger(__name__)


def get_literal_type(literal: Literal) -> URIRef:
    if literal.datatype is not None:
        return literal.datatype

    else:
        val = literal.value
        try:
            int(val)

            return XSD.int
        except ValueError:
            try:
                float(val)

                return XSD.float
            except ValueError:
                try:
                    date_time = pd.to_datetime(val, format='mixed')

                    if date_time.time == time(0, 0):
                        return XSD.date

                    else:
                        return XSD.dateTime

                except ValueError:
                    return XSD.string


def get_column(dtype: TypeHandler) -> LabeledColumn:
    if dtype.iri in [XSD.int, XSD.positiveInteger, XSD.integer, XSD.nonNegativeInteger]:

        if len(dtype.values) > 0:
            int_values = []
            for value in dtype.values:
                try:
                    int_value = int(value)
                    int_values.append(int_value)
                except (ValueError, TypeError):
                    continue

            min_value = min(int_values)
            avg_value = sum(int_values) / len(int_values)
            max_value = max(int_values)
            value_std_dev = float(np.std(int_values))

            return IntegerColumn(
                column_name=dtype.id_,
                min_value=min_value,
                avg_value=avg_value,
                max_value=max_value,
                value_stddev=value_std_dev
            )

        else:
            return IntegerColumn(dtype.id_, 0, 0., 0, 0.)

    elif dtype.iri in [XSD.decimal, XSD.float, XSD.double]:
        if len(dtype.values) > 0:
            float_values = []

            for value_str in dtype.values:
                try:
                    float_value = float(value_str)
                    float_values.append(float_value)
                except (ValueError, TypeError):
                    continue

            min_value = min(float_values)
            avg_value = sum(float_values) / len(float_values)
            max_value = max(float_values)
            value_std_dev = float(np.std(float_values))

            return FloatColumn(
                column_name=dtype.id_,
                min_value=min_value,
                avg_value=avg_value,
                max_value=max_value,
                value_stddev=value_std_dev
            )

        else:
            return FloatColumn(dtype.id_, 0., 0., 0., 0.)

    elif dtype.iri in [XSD.dateTime, XSD.date]:
        if len(dtype.values) > 0:

            timestamp_values = []
            for s in dtype.values:
                try:
                    timestamp_values.append(pd.to_datetime(s, format='mixed').tz_localize(None))
                except:
                    logger.error(f'{s} cannot be converted to date time')
                    continue

            date_time_series: Series = pd.Series(
                [t for t in timestamp_values if isinstance(t, Timestamp)]
            )

            return DateTimeColumn(
                column_name=dtype.id_,
                min_date_time=date_time_series.min(),
                mean_date_time=date_time_series.mean(),
                max_date_time=date_time_series.max()
            )

        else:
            now = Timestamp.now()
            return DateTimeColumn(dtype.id_, now, now, now)

    elif dtype.iri == XSD.boolean:
        if len(dtype.values) > 0:
            bool_values = []

            for value in dtype.values:
                if str(value).lower() == 'true':
                    bool_values.append(True)
                elif str(value).lower() == 'false':
                    bool_values.append(False)
                elif str(value).isnumeric():
                    bool_values.append(bool(int(value)))
                else:
                    bool_values.append(bool(value))

            num_true = len([b for b in bool_values if b is True])
            num_false = len([b for b in bool_values if b is False])
            num_total = num_true + num_false

            portion_true = num_true / num_total
            portion_false = num_false / num_total

            return BooleanColumn(
                column_name=dtype.id_,
                portion_true=portion_true,
                portion_false=portion_false
            )

        else:
            return BooleanColumn(dtype.id_, 0., 0.)

    elif dtype.iri == XSD.string:
        if len(dtype.values) > 0:
            value_lengths = []
            num_spaces = 0

            for value in dtype.values:
                try:
                    value_len = len(value)
                    if ' ' in value:
                        num_spaces += 1
                    value_lengths.append(value_len)
                except TypeError:
                    continue

            min_value_len = min(value_lengths)
            avg_value_len = sum(value_lengths) / len(value_lengths)
            max_value_len = max(value_lengths)

            if num_spaces > 0:
                return TextColumn(
                    column_name=dtype.id_,
                    min_text_length=min_value_len,
                    avg_text_length=avg_value_len,
                    max_text_length=max_value_len
                )

            else:
                return StringColumn(
                    column_name=dtype.id_,
                    min_str_length=min_value_len,
                    avg_str_length=avg_value_len,
                    max_str_length=max_value_len
                )
        else:
            return StringColumn(dtype.id_, 0, 0., 0)

    elif dtype.iri == XSD.anyURI:
        if len(dtype.values) > 0:
            id_lengths = list(map(lambda s: len(str(s)), dtype.values))

            min_id_len = min(id_lengths)
            avg_id_len = sum(id_lengths) / len(id_lengths)
            max_id_len = max(id_lengths)

            return TypedIDColumn(
                column_name=dtype.id_,
                min_id_length=min_id_len,
                avg_id_length=avg_id_len,
                max_id_length=max_id_len
            )

        else:
            return TypedIDColumn(dtype.id_, 0, 0., 0)

    # http://www.opengis.net/ont/geosparql#wktLiteral ? These contain actually two columns
    else:
        logger.error(f'Column generation for {dtype.iri} not implemented, yet')
