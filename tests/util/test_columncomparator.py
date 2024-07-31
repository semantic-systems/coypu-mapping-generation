from pandas import Timestamp

from pytest import approx

from util.columncomparator import UncomparableException
from semanticlabeling.labeledcolumn import BooleanColumn, CategoriesColumn, \
    DateTimeColumn, FloatColumn, IDColumn, IntegerColumn, StringColumn, \
    TextColumn, TypedIDColumn, UntypedIDColumn, WGS84CoordinateColumn, \
    WGS84LatitudeColumn, WGS84LongitudeColumn, YetUnknownTypeColumn


def test_compare_id_id():
    id_column_01 = IDColumn(
        'test ID column 1',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    id_column_02 = IDColumn(
        'test ID column 2',
        min_id_length=6,
        avg_id_length=9,
        max_id_length=12
    )

    try:
        diff = id_column_01 - id_column_02
        assert True
    except UncomparableException:
        assert False

    assert diff == 3 + 4 + 0


def test_compare_id_untyped_id():
    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    untyped_id_column = UntypedIDColumn()

    try:
        id_column - untyped_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_id_typed_id():
    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    try:
        res = id_column - typed_id_column
        assert True
    except UncomparableException:
        assert False

    assert res == 1 + 1 + 1


def test_compare_id_text():
    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    try:
        id_column - text_column
        assert False
    except UncomparableException:
        assert True


def test_compare_id_string():
    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    str_column = StringColumn(
        'test string column',
        min_str_length=4,
        avg_str_length=8.3,
        max_str_length=34
    )

    try:
        id_column - str_column
        assert False
    except UncomparableException:
        assert True


def test_compare_id_category():
    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    try:
        id_column - categories_column
        assert False
    except UncomparableException:
        assert True


def test_compare_id_bool():
    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    try:
        id_column - bool_column
        assert False
    except UncomparableException:
        assert True


def test_compare_id_int():
    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    try:
        id_column - int_column
        assert False
    except UncomparableException:
        assert True


def test_compare_id_float():
    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    float_column = FloatColumn(
        'test float column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        id_column - float_column
        assert False
    except UncomparableException:
        assert True


def test_compare_id_wgs84_coordinate():
    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        id_column - wgs84_coordinate_column
        assert False
    except UncomparableException:
        assert True


def test_compare_id_wgs84_lat():
    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        id_column - wgs84_lat_column
        assert False
    except UncomparableException:
        assert True


def test_compare_id_wgs84_lon():
    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        id_column - wgs84_lon_column
        assert False
    except UncomparableException:
        assert True


def test_compare_id_datetime():
    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    try:
        id_column - datetime_column
        assert False
    except UncomparableException:
        assert True


def test_compare_id_unknown():
    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    try:
        id_column - unknown_type_column
        assert False
    except UncomparableException:
        assert True


def test_compare_untyped_id_id():
    untyped_id_column = UntypedIDColumn()

    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    try:
        untyped_id_column - id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_untyped_id_untyped_id():
    untyped_id_column_01 = UntypedIDColumn()
    untyped_id_column_02 = UntypedIDColumn()

    try:
        untyped_id_column_01 - untyped_id_column_02
        assert False
    except UncomparableException:
        assert True


def test_compare_untyped_id_typed_id():
    untyped_id_column = UntypedIDColumn()

    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    try:
        untyped_id_column - typed_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_untyped_id_text():
    untyped_id_column = UntypedIDColumn()

    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    try:
        untyped_id_column - text_column
        assert False
    except UncomparableException:
        assert True


def test_compare_untyped_id_string():
    untyped_id_column = UntypedIDColumn()

    str_column = StringColumn(
        'test string column',
        min_str_length=4,
        avg_str_length=8.3,
        max_str_length=34
    )

    try:
        untyped_id_column - str_column
        assert False
    except UncomparableException:
        assert True


def test_compare_untyped_id_category():
    untyped_id_column = UntypedIDColumn()

    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    try:
        untyped_id_column - categories_column
        assert False
    except UncomparableException:
        assert True


def test_compare_untyped_id_bool():
    untyped_id_column = UntypedIDColumn()

    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    try:
        untyped_id_column - bool_column
        assert False
    except UncomparableException:
        assert True


def test_compare_untyped_id_int():
    untyped_id_column = UntypedIDColumn()

    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    try:
        untyped_id_column - int_column
        assert False
    except UncomparableException:
        assert True


def test_compare_untyped_id_float():
    untyped_id_column = UntypedIDColumn()

    float_column = FloatColumn(
        'test float column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        untyped_id_column - float_column
        assert False
    except UncomparableException:
        assert True


def test_compare_untyped_id_wgs84_coordinate():
    untyped_id_column = UntypedIDColumn()

    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        untyped_id_column - wgs84_coordinate_column
        assert False
    except UncomparableException:
        assert True


def test_compare_untyped_id_wgs84_lat():
    untyped_id_column = UntypedIDColumn()

    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        untyped_id_column - wgs84_lat_column
        assert False
    except UncomparableException:
        assert True


def test_compare_untyped_id_wgs84_lon():
    untyped_id_column = UntypedIDColumn()

    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        untyped_id_column - wgs84_lon_column
        assert False
    except UncomparableException:
        assert True


def test_compare_untyped_id_datetime():
    untyped_id_column = UntypedIDColumn()

    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    try:
        untyped_id_column - datetime_column
        assert False
    except UncomparableException:
        assert True


def test_compare_untyped_id_unknown():
    untyped_id_column = UntypedIDColumn()
    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    try:
        untyped_id_column - unknown_type_column
        assert False
    except UncomparableException:
        assert True


def test_compare_typed_id_id():
    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    try:
        diff = typed_id_column - id_column
        assert True
    except UncomparableException:
        assert False

    assert diff == 1 + 1 + 1


def test_compare_typed_id_untyped_id():
    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    untyped_id_column = UntypedIDColumn()

    try:
        typed_id_column - untyped_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_typed_id_typed_id():
    typed_id_column_01 = TypedIDColumn(
        'test typed ID column 1',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    typed_id_column_02 = TypedIDColumn(
        'test typed ID column 2',
        min_id_length=1,  # diff 1
        avg_id_length=7,  # diff 1
        max_id_length=11  # diff 2
    )

    try:
        diff = typed_id_column_01 - typed_id_column_02
        assert True
    except UncomparableException:
        assert False

    assert diff == 1 + 1 + 2


def test_compare_typed_id_text():
    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    try:
        typed_id_column - text_column
        assert False
    except UncomparableException:
        assert True


def test_compare_typed_id_string():
    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    str_column = StringColumn(
        'test string column',
        min_str_length=4,
        avg_str_length=8.3,
        max_str_length=34
    )

    try:
        typed_id_column - str_column
        assert False
    except UncomparableException:
        assert True


def test_compare_typed_id_category():
    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    try:
        typed_id_column - categories_column
        assert False
    except UncomparableException:
        assert True


def test_compare_typed_id_bool():
    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    try:
        typed_id_column - bool_column
        assert False
    except UncomparableException:
        assert True


def test_compare_typed_id_int():
    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    try:
        typed_id_column - int_column
        assert False
    except UncomparableException:
        assert True


def test_compare_typed_id_float():
    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    float_column = FloatColumn(
        'test float column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        typed_id_column - float_column
        assert False
    except UncomparableException:
        assert True


def test_compare_typed_id_wgs84_coordinate():
    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        typed_id_column - wgs84_coordinate_column
        assert False
    except UncomparableException:
        assert True


def test_compare_typed_id_wgs84_lat():
    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        typed_id_column - wgs84_lat_column
        assert False
    except UncomparableException:
        assert True


def test_compare_typed_id_wgs84_lon():
    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        typed_id_column - wgs84_lon_column
        assert False
    except UncomparableException:
        assert True


def test_compare_typed_id_datetime():
    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    try:
        typed_id_column - datetime_column
        assert False
    except UncomparableException:
        assert True


def test_compare_typed_id_unknown():
    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    try:
        typed_id_column - unknown_type_column
        assert False
    except UncomparableException:
        assert True


def test_compare_text_id():
    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    try:
        text_column - id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_text_untyped_id():
    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    untyped_id_column = UntypedIDColumn()

    try:
        text_column - untyped_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_text_typed_id():
    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    try:
        text_column - typed_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_text_text():
    text_column_01 = TextColumn(
        'test text column 1',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    text_column_02 = TextColumn(
        'test text column 2',
        min_text_length=11,  # diff 1
        avg_text_length=35.6,  # diff 1.1
        max_text_length=118  # diff 2
    )

    try:
        diff = text_column_01 - text_column_02
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(1 + 1.1 + 2)


def test_compare_text_string():
    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    str_column = StringColumn(
        'test string column',
        min_str_length=4,  # diff 8
        avg_str_length=8.3,  # diff 26.2
        max_str_length=34  # diff 86
    )

    try:
        diff = text_column - str_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(8 + 26.2 + 86)


def test_compare_text_category():
    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    try:
        text_column - categories_column
        assert False
    except UncomparableException:
        assert True


def test_compare_text_bool():
    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    try:
        text_column - bool_column
        assert False
    except UncomparableException:
        assert True


def test_compare_text_int():
    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    try:
        text_column - int_column
        assert False
    except UncomparableException:
        assert True


def test_compare_text_float():
    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    float_column = FloatColumn(
        'test float column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        text_column - float_column
        assert False
    except UncomparableException:
        assert True


def test_compare_text_wgs84_coordinate():
    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        text_column - wgs84_coordinate_column
        assert False
    except UncomparableException:
        assert True


def test_compare_text_wgs84_lat():
    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        text_column - wgs84_lat_column
        assert False
    except UncomparableException:
        assert True


def test_compare_text_wgs84_lon():
    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        text_column - wgs84_lon_column
        assert False
    except UncomparableException:
        assert True


def test_compare_text_datetime():
    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    try:
        text_column - datetime_column
        assert False
    except UncomparableException:
        assert True


def test_compare_text_unknown():
    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    try:
        text_column - unknown_type_column
        assert False
    except UncomparableException:
        assert True


def test_compare_string_id():
    str_column = StringColumn(
        'test string column',
        min_str_length=4,
        avg_str_length=8.3,
        max_str_length=34
    )

    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    try:
        str_column - id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_string_untyped_id():
    str_column = StringColumn(
        'test string column',
        min_str_length=4,
        avg_str_length=8.3,
        max_str_length=34
    )

    untyped_id_column = UntypedIDColumn()

    try:
        str_column - untyped_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_string_typed_id():
    str_column = StringColumn(
        'test string column',
        min_str_length=4,
        avg_str_length=8.3,
        max_str_length=34
    )

    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    try:
        str_column - typed_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_string_text():
    str_column = StringColumn(
        'test string column',
        min_str_length=4,
        avg_str_length=8.3,
        max_str_length=34
    )

    text_column = TextColumn(
        'test text column',
        min_text_length=12,  # diff 8
        avg_text_length=34.5,  # 26.2
        max_text_length=120  # 86
    )

    try:
        diff = str_column - text_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(8 + 26.2 + 86)


def test_compare_string_string():
    str_column_01 = StringColumn(
        'test string column 1',
        min_str_length=4,
        avg_str_length=8.3,
        max_str_length=34
    )

    str_column_02 = StringColumn(
        'test string column 2',
        min_str_length=3,  # diff 1
        avg_str_length=9.4,  # diff 1.1
        max_str_length=32  # diff 2
    )

    try:
        diff = str_column_01 - str_column_02
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(1 + 1.1 + 2)


def test_compare_string_category():
    str_column = StringColumn(
        'test string column',
        min_str_length=4,
        avg_str_length=8.3,
        max_str_length=34
    )

    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    try:
        str_column - categories_column
        assert False
    except UncomparableException:
        assert True


def test_compare_string_bool():
    str_column = StringColumn(
        'test string column',
        min_str_length=4,
        avg_str_length=8.3,
        max_str_length=34
    )

    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    try:
        str_column - bool_column
        assert False
    except UncomparableException:
        assert True


def test_compare_string_int():
    str_column = StringColumn(
        'test string column',
        min_str_length=4,
        avg_str_length=8.3,
        max_str_length=34
    )

    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    try:
        str_column - int_column
        assert False
    except UncomparableException:
        assert True


def test_compare_string_float():
    str_column = StringColumn(
        'test string column',
        min_str_length=4,
        avg_str_length=8.3,
        max_str_length=34
    )

    float_column = FloatColumn(
        'test float column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        str_column - float_column
        assert False
    except UncomparableException:
        assert True


def test_compare_string_wgs84_coordinate():
    str_column = StringColumn(
        'test string column',
        min_str_length=4,
        avg_str_length=8.3,
        max_str_length=34
    )

    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        str_column - wgs84_coordinate_column
        assert False
    except UncomparableException:
        assert True


def test_compare_string_wgs84_lat():
    str_column = StringColumn(
        'test string column',
        min_str_length=4,
        avg_str_length=8.3,
        max_str_length=34
    )

    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        str_column - wgs84_lat_column
        assert False
    except UncomparableException:
        assert True


def test_compare_string_wgs84_lon():
    str_column = StringColumn(
        'test string column',
        min_str_length=4,
        avg_str_length=8.3,
        max_str_length=34
    )

    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        str_column - wgs84_lon_column
        assert False
    except UncomparableException:
        assert True


def test_compare_string_datetime():
    str_column = StringColumn(
        'test string column',
        min_str_length=4,
        avg_str_length=8.3,
        max_str_length=34
    )

    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    try:
        str_column - datetime_column
        assert False
    except UncomparableException:
        assert True


def test_compare_string_unknown():
    str_column = StringColumn(
        'test string column',
        min_str_length=4,
        avg_str_length=8.3,
        max_str_length=34
    )

    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    try:
        str_column - unknown_type_column
        assert False
    except UncomparableException:
        assert True


def test_compare_category_id():
    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    try:
        categories_column - id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_category_untyped_id():
    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    untyped_id_column = UntypedIDColumn()

    try:
        categories_column - untyped_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_category_typed_id():
    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    try:
        categories_column - typed_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_category_text():
    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    text_column = TextColumn(
        'test text column',
        min_text_length=12,  # diff 8
        avg_text_length=34.5,  # 26.2
        max_text_length=120  # 86
    )

    try:
        categories_column - text_column
        assert False
    except UncomparableException:
        assert True


def test_compare_category_string():
    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    str_column_02 = StringColumn(
        'test string column 2',
        min_str_length=3,  # diff 1
        avg_str_length=9.4,  # diff 1.1
        max_str_length=32  # diff 2
    )

    try:
        categories_column - str_column_02
        assert False
    except UncomparableException:
        assert True


def test_compare_category_category():
    categories_column_01 = CategoriesColumn(
        'test categories column 1',
        ['category 1', 'category 2', 'category 3']
    )

    categories_column_02 = CategoriesColumn(
        'test categories column 2',
        ['category 1', 'category 2', 'category 3']
    )

    categories_column_03 = CategoriesColumn(
        'test categories column 3',
        ['category 3', 'category 4', 'category 5']
    )

    categories_column_04 = CategoriesColumn(
        'test categories column 4',
        ['category 6', 'category 7', 'category 8']
    )

    try:
        # identical sets of categories --> diff == 0
        diff = categories_column_01 - categories_column_02
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(0)

    try:
        # category overlap of 1 --> diff == 1 - (1/5)
        diff = categories_column_01 - categories_column_03
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(1-(1/5))

    try:
        # disjoint sets of categories --> diff == 1
        diff = categories_column_01 - categories_column_04
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(1)


def test_compare_category_bool():
    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    try:
        categories_column - bool_column
        assert False
    except UncomparableException:
        assert True


def test_compare_category_int():
    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    try:
        categories_column - int_column
        assert False
    except UncomparableException:
        assert True


def test_compare_category_float():
    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    float_column = FloatColumn(
        'test float column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        categories_column - float_column
        assert False
    except UncomparableException:
        assert True


def test_compare_category_wgs84_coordinate():
    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        categories_column - wgs84_coordinate_column
        assert False
    except UncomparableException:
        assert True


def test_compare_category_wgs84_lat():
    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        categories_column - wgs84_lat_column
        assert False
    except UncomparableException:
        assert True


def test_compare_category_wgs84_lon():
    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        categories_column - wgs84_lon_column
        assert False
    except UncomparableException:
        assert True


def test_compare_category_datetime():
    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    try:
        categories_column - datetime_column
        assert False
    except UncomparableException:
        assert True


def test_compare_category_unknown():
    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    try:
        categories_column - unknown_type_column
        assert False
    except UncomparableException:
        assert True


def test_compare_bool_id():
    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    try:
        bool_column - id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_bool_untyped_id():
    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    untyped_id_column = UntypedIDColumn()

    try:
        bool_column - untyped_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_bool_typed_id():
    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    try:
        bool_column - typed_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_bool_text():
    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    try:
        bool_column - text_column
        assert False
    except UncomparableException:
        assert True


def test_compare_bool_string():
    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    str_column = StringColumn(
        'test string column',
        min_str_length=3,
        avg_str_length=9.4,
        max_str_length=32
    )

    try:
        bool_column - str_column
        assert False
    except UncomparableException:
        assert True


def test_compare_bool_category():
    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    try:
        bool_column - categories_column
        assert False
    except UncomparableException:
        assert True


def test_compare_bool_bool():
    bool_column_01 = BooleanColumn(
        'test boolean column 1',
        portion_true=0.7,
        portion_false=0.3
    )

    bool_column_02 = BooleanColumn(
        'test boolean column 2',
        portion_true=0.4,  # diff 0.3
        portion_false=0.6  # diff 0.3
    )

    try:
        diff = bool_column_01 - bool_column_02
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(0.3 + 0.3)


def test_compare_bool_int():
    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    try:
        bool_column - int_column
        assert False
    except UncomparableException:
        assert True


def test_compare_bool_float():
    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    float_column = FloatColumn(
        'test float column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        bool_column - float_column
        assert False
    except UncomparableException:
        assert True


def test_compare_bool_wgs84_coordinate():
    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        bool_column - wgs84_coordinate_column
        assert False
    except UncomparableException:
        assert True


def test_compare_bool_wgs84_lat():
    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        bool_column - wgs84_lat_column
        assert False
    except UncomparableException:
        assert True


def test_compare_bool_wgs84_lon():
    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    try:
        bool_column - wgs84_lon_column
        assert False
    except UncomparableException:
        assert True


def test_compare_bool_datetime():
    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    try:
        bool_column - datetime_column
        assert False
    except UncomparableException:
        assert True


def test_compare_bool_unknown():
    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    try:
        bool_column - unknown_type_column
        assert False
    except UncomparableException:
        assert True


def test_compare_int_id():
    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    try:
        int_column - id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_int_untyped_id():
    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    untyped_id_column = UntypedIDColumn()

    try:
        int_column - untyped_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_int_typed_id():
    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    try:
        int_column - typed_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_int_text():
    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    try:
        int_column - text_column
        assert False
    except UncomparableException:
        assert True


def test_compare_int_string():
    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    str_column = StringColumn(
        'test string column',
        min_str_length=3,
        avg_str_length=9.4,
        max_str_length=32
    )

    try:
        int_column - str_column
        assert False
    except UncomparableException:
        assert True


def test_compare_int_category():
    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    try:
        int_column - categories_column
        assert False
    except UncomparableException:
        assert True


def test_compare_int_bool():
    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    try:
        int_column - bool_column
        assert False
    except UncomparableException:
        assert True


def test_compare_int_int():
    int_column_01 = IntegerColumn(
        'test integer column 1',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    int_column_02 = IntegerColumn(
        'test integer column 2',
        min_value=36,  # diff 2
        avg_value=46.7,  # diff 1.1
        max_value=122,  # diff 1
        value_stddev=44.9  # diff 0.4
    )

    try:
        diff = int_column_01 - int_column_02
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(2 + 1.1 + 1 + 0.4)


def test_compare_int_float():
    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    float_column = FloatColumn(
        'test float column',
        min_value=12.3,  # diff 21.7
        avg_value=34.5,  # diff 11.1
        max_value=123.4,  # diff 0.4
        value_stddev=54.3  # diff 9
    )

    try:
        diff = int_column - float_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(21.7 + 11.1 + 0.4 + 9)


def test_compare_int_wgs84_coordinate():
    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,  # diff 21.7
        avg_value=34.5,  # diff 11.1
        max_value=123.4,  # diff 0.4
        value_stddev=54.3  # diff 9
    )

    try:
        diff = int_column - wgs84_coordinate_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(21.7 + 11.1 + 0.4 + 9)


def test_compare_int_wgs84_lat():
    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,  # diff 21.7
        avg_value=34.5,  # diff 11.1
        max_value=123.4,  # diff 0.4
        value_stddev=54.3  # diff 9
    )

    try:
        diff = int_column - wgs84_lat_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(21.7 + 11.1 + 0.4 + 9)


def test_compare_int_wgs84_lon():
    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,  # diff 21.7
        avg_value=34.5,  # diff 11.1
        max_value=123.4,  # diff 0.4
        value_stddev=54.3  # diff 9
    )

    try:
        diff = int_column - wgs84_lon_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(21.7 + 11.1 + 0.4 + 9)


def test_compare_int_datetime():
    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    try:
        int_column - datetime_column
        assert False
    except UncomparableException:
        assert True


def test_compare_int_unknown():
    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    try:
        int_column - unknown_type_column
        assert False
    except UncomparableException:
        assert True


def test_compare_float_id():
    float_column = FloatColumn(
        'test float column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    try:
        float_column - id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_float_untyped_id():
    float_column = FloatColumn(
        'test float column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    untyped_id_column = UntypedIDColumn()

    try:
        float_column - untyped_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_float_typed_id():
    float_column = FloatColumn(
        'test float column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    try:
        float_column - typed_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_float_text():
    float_column = FloatColumn(
        'test float column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    try:
        float_column - text_column
        assert False
    except UncomparableException:
        assert True


def test_compare_float_string():
    float_column = FloatColumn(
        'test float column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    str_column = StringColumn(
        'test string column',
        min_str_length=3,
        avg_str_length=9.4,
        max_str_length=32
    )

    try:
        float_column - str_column
        assert False
    except UncomparableException:
        assert True


def test_compare_float_category():
    float_column = FloatColumn(
        'test float column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    try:
        float_column - categories_column
        assert False
    except UncomparableException:
        assert True


def test_compare_float_bool():
    float_column = FloatColumn(
        'test float column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    try:
        float_column - bool_column
        assert False
    except UncomparableException:
        assert True


def test_compare_float_int():
    float_column = FloatColumn(
        'test float column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    int_column = IntegerColumn(
        'test integer column',
        min_value=34,  # diff 21.7
        avg_value=45.6,  # diff 11.1
        max_value=123,  # diff 0.4
        value_stddev=45.3  # diff 9
    )

    try:
        diff = float_column - int_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(21.7 + 11.1 + 0.4 + 9)


def test_compare_float_float():
    float_column_01 = FloatColumn(
        'test float column 1',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    float_column_02 = FloatColumn(
        'test float column 2',
        min_value=11.3,  # diff 1
        avg_value=35.1,  # diff 0.6
        max_value=96.5,  # diff 26.9
        value_stddev=38.1  # diff 16.2
    )

    try:
        diff = float_column_01 - float_column_02
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(1 + 0.6 + 26.9 + 16.2)


def test_compare_float_wgs84_coordinate():
    float_column = FloatColumn(
        'test float column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=11.3,  # diff 1
        avg_value=35.1,  # diff 0.6
        max_value=96.5,  # diff 26.9
        value_stddev=38.1  # diff 16.2
    )

    try:
        diff = float_column - wgs84_coordinate_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(1 + 0.6 + 26.9 + 16.2)


def test_compare_float_wgs84_lat():
    float_column = FloatColumn(
        'test float column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=11.3,  # diff 1
        avg_value=35.1,  # diff 0.6
        max_value=96.5,  # diff 26.9
        value_stddev=38.1  # diff 16.2
    )

    try:
        diff = float_column - wgs84_lat_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(1 + 0.6 + 26.9 + 16.2)


def test_compare_float_wgs84_lon():
    float_column = FloatColumn(
        'test float column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=11.3,  # diff 1
        avg_value=35.1,  # diff 0.6
        max_value=96.5,  # diff 26.9
        value_stddev=38.1  # diff 16.2
    )

    try:
        diff = float_column - wgs84_lon_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(1 + 0.6 + 26.9 + 16.2)


def test_compare_float_datetime():
    float_column = FloatColumn(
        'test float column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    try:
        float_column - datetime_column
        assert False
    except UncomparableException:
        assert True


def test_compare_float_unknown():
    float_column = FloatColumn(
        'test float column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    try:
        float_column - unknown_type_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_coordinate_id():
    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    try:
        wgs84_coordinate_column - id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_coordinate_untyped_id():
    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    untyped_id_column = UntypedIDColumn()

    try:
        wgs84_coordinate_column - untyped_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_coordinate_typed_id():
    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    try:
        wgs84_coordinate_column - typed_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_coordinate_text():
    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    try:
        wgs84_coordinate_column - text_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_coordinate_string():
    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    str_column = StringColumn(
        'test string column',
        min_str_length=3,
        avg_str_length=9.4,
        max_str_length=32
    )

    try:
        wgs84_coordinate_column - str_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_coordinate_category():
    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    try:
        wgs84_coordinate_column - categories_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_coordinate_bool():
    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    try:
        wgs84_coordinate_column - bool_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_coordinate_int():
    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    int_column = IntegerColumn(
        'test integer column',
        min_value=34,  # diff 21.7
        avg_value=45.6,  # diff 11.1
        max_value=123,  # diff 0.4
        value_stddev=45.3  # diff 9
    )

    try:
        diff = wgs84_coordinate_column - int_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(21.7 + 11.1 + 0.4 + 9)


def test_compare_wgs84_coordinate_float():
    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    float_column = FloatColumn(
        'test float column',
        min_value=11.3,  # diff 1
        avg_value=35.1,  # diff 0.6
        max_value=96.5,  # diff 26.9
        value_stddev=38.1  # diff 16.2
    )

    try:
        diff = wgs84_coordinate_column - float_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(1 + 0.6 + 26.9 + 16.2)


def test_compare_wgs84_coordinate_wgs84_coordinate():
    wgs84_coordinate_column_01 = WGS84CoordinateColumn(
        'test WGS 84 column 1',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    wgs84_coordinate_column_02 = WGS84CoordinateColumn(
        'test WGS 84 column 2',
        min_value=11.3,  # diff 1
        avg_value=35.1,  # diff 0.6
        max_value=96.5,  # diff 26.9
        value_stddev=38.1  # diff 16.2
    )

    try:
        diff = wgs84_coordinate_column_01 - wgs84_coordinate_column_02
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(1 + 0.6 + 26.9 + 16.2)


def test_compare_wgs84_coordinate_wgs84_lat():
    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=11.3,  # diff 1
        avg_value=35.1,  # diff 0.6
        max_value=96.5,  # diff 26.9
        value_stddev=38.1  # diff 16.2
    )

    try:
        diff = wgs84_coordinate_column - wgs84_lat_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(1 + 0.6 + 26.9 + 16.2)


def test_compare_wgs84_coordinate_wgs84_lon():
    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=11.3,  # diff 1
        avg_value=35.1,  # diff 0.6
        max_value=96.5,  # diff 26.9
        value_stddev=38.1  # diff 16.2
    )

    try:
        diff = wgs84_coordinate_column - wgs84_lon_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(1 + 0.6 + 26.9 + 16.2)


def test_compare_wgs84_coordinate_datetime():
    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    try:
        wgs84_coordinate_column - datetime_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_coordinate_unknown():
    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    try:
        wgs84_coordinate_column - unknown_type_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_lat_id():
    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    try:
        wgs84_lat_column - id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_lat_untyped_id():
    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    untyped_id_column = UntypedIDColumn()

    try:
        wgs84_lat_column - untyped_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_lat_typed_id():
    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    try:
        wgs84_lat_column - typed_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_lat_text():
    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    try:
        wgs84_lat_column - text_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_lat_string():
    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    str_column = StringColumn(
        'test string column',
        min_str_length=3,
        avg_str_length=9.4,
        max_str_length=32
    )

    try:
        wgs84_lat_column - str_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_lat_category():
    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    try:
        wgs84_lat_column - categories_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_lat_bool():
    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    try:
        wgs84_lat_column - bool_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_lat_int():
    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    int_column = IntegerColumn(
        'test integer column',
        min_value=34,  # diff 21.7
        avg_value=45.6,  # diff 11.1
        max_value=123,  # diff 0.4
        value_stddev=45.3  # diff 9
    )

    try:
        diff = wgs84_lat_column - int_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(21.7 + 11.1 + 0.4 + 9)


def test_compare_wgs84_lat_float():
    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    float_column = FloatColumn(
        'test float column',
        min_value=11.3,  # diff 1
        avg_value=35.1,  # diff 0.6
        max_value=96.5,  # diff 26.9
        value_stddev=38.1  # diff 16.2
    )

    try:
        diff = wgs84_lat_column - float_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(1 + 0.6 + 26.9 + 16.2)


def test_compare_wgs84_lat_wgs84_coordinate():
    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=11.3,  # diff 1
        avg_value=35.1,  # diff 0.6
        max_value=96.5,  # diff 26.9
        value_stddev=38.1  # diff 16.2
    )

    try:
        diff = wgs84_lat_column - wgs84_coordinate_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(1 + 0.6 + 26.9 + 16.2)


def test_compare_wgs84_lat_wgs84_lat():
    wgs84_lat_column_01 = WGS84LatitudeColumn(
        'test WGS 84 column 1',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    wgs84_lat_column_02 = WGS84LatitudeColumn(
        'test WGS 84 column 2',
        min_value=11.3,  # diff 1
        avg_value=35.1,  # diff 0.6
        max_value=96.5,  # diff 26.9
        value_stddev=38.1  # diff 16.2
    )

    try:
        diff = wgs84_lat_column_01 - wgs84_lat_column_02
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(1 + 0.6 + 26.9 + 16.2)


def test_compare_wgs84_lat_wgs84_lon():
    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=11.3,  # diff 1
        avg_value=35.1,  # diff 0.6
        max_value=96.5,  # diff 26.9
        value_stddev=38.1  # diff 16.2
    )

    try:
        diff = wgs84_lat_column - wgs84_lon_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(1 + 0.6 + 26.9 + 16.2)


def test_compare_wgs84_lat_datetime():
    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    try:
        wgs84_lat_column - datetime_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_lat_unknown():
    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    try:
        wgs84_lat_column - unknown_type_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_lon_id():
    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    try:
        wgs84_lon_column - id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_lon_untyped_id():
    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    untyped_id_column = UntypedIDColumn()

    try:
        wgs84_lon_column - untyped_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_lon_typed_id():
    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    try:
        wgs84_lon_column - typed_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_lon_text():
    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    try:
        wgs84_lon_column - text_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_lon_string():
    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    str_column = StringColumn(
        'test string column',
        min_str_length=3,
        avg_str_length=9.4,
        max_str_length=32
    )

    try:
        wgs84_lon_column - str_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_lon_category():
    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    try:
        wgs84_lon_column - categories_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_lon_bool():
    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    try:
        wgs84_lon_column - bool_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_lon_int():
    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    int_column = IntegerColumn(
        'test integer column',
        min_value=34,  # diff 21.7
        avg_value=45.6,  # diff 11.1
        max_value=123,  # diff 0.4
        value_stddev=45.3  # diff 9
    )

    try:
        diff = wgs84_lon_column - int_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(21.7 + 11.1 + 0.4 + 9)


def test_compare_wgs84_lon_float():
    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    float_column = FloatColumn(
        'test float column',
        min_value=11.3,  # diff 1
        avg_value=35.1,  # diff 0.6
        max_value=96.5,  # diff 26.9
        value_stddev=38.1  # diff 16.2
    )

    try:
        diff = wgs84_lon_column - float_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(1 + 0.6 + 26.9 + 16.2)


def test_compare_wgs84_lon_wgs84_coordinate():
    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=11.3,  # diff 1
        avg_value=35.1,  # diff 0.6
        max_value=96.5,  # diff 26.9
        value_stddev=38.1  # diff 16.2
    )

    try:
        diff = wgs84_lon_column - wgs84_coordinate_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(1 + 0.6 + 26.9 + 16.2)


def test_compare_wgs84_lon_wgs84_lat():
    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=11.3,  # diff 1
        avg_value=35.1,  # diff 0.6
        max_value=96.5,  # diff 26.9
        value_stddev=38.1  # diff 16.2
    )

    try:
        diff = wgs84_lon_column - wgs84_lat_column
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(1 + 0.6 + 26.9 + 16.2)


def test_compare_wgs84_lon_wgs84_lon():
    wgs84_lon_column_01 = WGS84LongitudeColumn(
        'test WGS 84 column 1',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    wgs84_lon_column_02 = WGS84LongitudeColumn(
        'test WGS 84 column 2',
        min_value=11.3,  # diff 1
        avg_value=35.1,  # diff 0.6
        max_value=96.5,  # diff 26.9
        value_stddev=38.1  # diff 16.2
    )

    try:
        diff = wgs84_lon_column_01 - wgs84_lon_column_02
        assert True
    except UncomparableException:
        assert False

    assert diff == approx(1 + 0.6 + 26.9 + 16.2)


def test_compare_wgs84_lon_datetime():
    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    try:
        wgs84_lon_column - datetime_column
        assert False
    except UncomparableException:
        assert True


def test_compare_wgs84_lon_unknown():
    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=12.3,
        avg_value=34.5,
        max_value=123.4,
        value_stddev=54.3
    )

    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    try:
        wgs84_lon_column - unknown_type_column
        assert False
    except UncomparableException:
        assert True


def test_compare_datetime_id():
    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    try:
        datetime_column - id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_datetime_untyped_id():
    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    untyped_id_column = UntypedIDColumn()

    try:
        datetime_column - untyped_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_datetime_typed_id():
    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    try:
        datetime_column - typed_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_datetime_text():
    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    try:
        datetime_column - text_column
        assert False
    except UncomparableException:
        assert True


def test_compare_datetime_string():
    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    str_column = StringColumn(
        'test string column',
        min_str_length=3,
        avg_str_length=9.4,
        max_str_length=32
    )

    try:
        datetime_column - str_column
        assert False
    except UncomparableException:
        assert True


def test_compare_datetime_category():
    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    try:
        datetime_column - categories_column
        assert False
    except UncomparableException:
        assert True


def test_compare_datetime_bool():
    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    try:
        datetime_column - bool_column
        assert False
    except UncomparableException:
        assert True


def test_compare_datetime_int():
    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    try:
        datetime_column - int_column
        assert False
    except UncomparableException:
        assert True


def test_compare_datetime_float():
    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    float_column = FloatColumn(
        'test float column',
        min_value=11.3,
        avg_value=35.1,
        max_value=96.5,
        value_stddev=38.1
    )

    try:
        datetime_column - float_column
        assert False
    except UncomparableException:
        assert True


def test_compare_datetime_wgs84_coordinate():
    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=11.3,
        avg_value=35.1,
        max_value=96.5,
        value_stddev=38.1
    )

    try:
        datetime_column - wgs84_coordinate_column
        assert False
    except UncomparableException:
        assert True


def test_compare_datetime_wgs84_lat():
    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=11.3,
        avg_value=35.1,
        max_value=96.5,
        value_stddev=38.1
    )

    try:
        datetime_column - wgs84_lat_column
        assert False
    except UncomparableException:
        assert True


def test_compare_datetime_wgs84_lon():
    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=11.3,
        avg_value=35.1,
        max_value=96.5,
        value_stddev=38.1
    )

    try:
        datetime_column - wgs84_lon_column
        assert False
    except UncomparableException:
        assert True


def test_compare_datetime_datetime():
    datetime_column_01 = DateTimeColumn(
        'test date time column 1',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    datetime_column_02 = DateTimeColumn(
        'test date time column 2',
        min_date_time=Timestamp.fromisoformat('2012-03-22T12:34:56'),  # diff 86400 = 1 * 24 * 60 * 60
        mean_date_time=Timestamp.fromisoformat('2018-09-11T11:20:46'),  # diff 7200 + 240 = 2 * 60 * 60 + 4 * 60
        max_date_time=Timestamp.fromisoformat('2022-04-02T23:45:02')  # diff 63158400
    )

    try:
        diff = datetime_column_01 - datetime_column_02
        assert True
    except UncomparableException:
        assert False

    assert diff == 86400 + (7200 + 240) + 63158400  # == 63252240


def test_compare_datetime_unknown():
    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    try:
        datetime_column - unknown_type_column
        assert False
    except UncomparableException:
        assert True


def test_compare_unknown_id():
    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    id_column = IDColumn(
        'test ID column',
        min_id_length=3,
        avg_id_length=5,
        max_id_length=12
    )

    try:
        unknown_type_column - id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_unknown_untyped_id():
    unknown_type_column = YetUnknownTypeColumn('test unknown type column')
    untyped_id_column = UntypedIDColumn()

    try:
        unknown_type_column - untyped_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_unknown_typed_id():
    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    typed_id_column = TypedIDColumn(
        'test typed ID column',
        min_id_length=2,
        avg_id_length=6,
        max_id_length=13
    )

    try:
        unknown_type_column - typed_id_column
        assert False
    except UncomparableException:
        assert True


def test_compare_unknown_text():
    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    text_column = TextColumn(
        'test text column',
        min_text_length=12,
        avg_text_length=34.5,
        max_text_length=120
    )

    try:
        unknown_type_column - text_column
        assert False
    except UncomparableException:
        assert True


def test_compare_unknown_string():
    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    str_column = StringColumn(
        'test string column',
        min_str_length=3,
        avg_str_length=9.4,
        max_str_length=32
    )

    try:
        unknown_type_column - str_column
        assert False
    except UncomparableException:
        assert True


def test_compare_unknown_category():
    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    categories_column = CategoriesColumn(
        'test categories column',
        ['category 1', 'category 2', 'category 3']
    )

    try:
        unknown_type_column - categories_column
        assert False
    except UncomparableException:
        assert True


def test_compare_unknown_bool():
    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    bool_column = BooleanColumn(
        'test boolean column',
        portion_true=0.7,
        portion_false=0.3
    )

    try:
        unknown_type_column - bool_column
        assert False
    except UncomparableException:
        assert True


def test_compare_unknown_int():
    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    int_column = IntegerColumn(
        'test integer column',
        min_value=34,
        avg_value=45.6,
        max_value=123,
        value_stddev=45.3
    )

    try:
        unknown_type_column - int_column
        assert False
    except UncomparableException:
        assert True


def test_compare_unknown_float():
    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    float_column = FloatColumn(
        'test float column',
        min_value=11.3,
        avg_value=35.1,
        max_value=96.5,
        value_stddev=38.1
    )

    try:
        unknown_type_column - float_column
        assert False
    except UncomparableException:
        assert True


def test_compare_unknown_wgs84_coordinate():
    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    wgs84_coordinate_column = WGS84CoordinateColumn(
        'test WGS 84 column',
        min_value=11.3,
        avg_value=35.1,
        max_value=96.5,
        value_stddev=38.1
    )

    try:
        unknown_type_column - wgs84_coordinate_column
        assert False
    except UncomparableException:
        assert True


def test_compare_unknown_wgs84_lat():
    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    wgs84_lat_column = WGS84LatitudeColumn(
        'test WGS 84 column',
        min_value=11.3,
        avg_value=35.1,
        max_value=96.5,
        value_stddev=38.1
    )

    try:
        unknown_type_column - wgs84_lat_column
        assert False
    except UncomparableException:
        assert True


def test_compare_unknown_wgs84_lon():
    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    wgs84_lon_column = WGS84LongitudeColumn(
        'test WGS 84 column',
        min_value=11.3,
        avg_value=35.1,
        max_value=96.5,
        value_stddev=38.1
    )

    try:
        unknown_type_column - wgs84_lon_column
        assert False
    except UncomparableException:
        assert True


def test_compare_unknown_datetime():
    unknown_type_column = YetUnknownTypeColumn('test unknown type column')

    datetime_column = DateTimeColumn(
        'test date time column',
        min_date_time=Timestamp.fromisoformat('2012-03-23T12:34:56'),
        mean_date_time=Timestamp.fromisoformat('2018-09-11T13:24:46'),
        max_date_time=Timestamp.fromisoformat('2024-04-02T23:45:02')
    )

    try:
        unknown_type_column - datetime_column
        assert False
    except UncomparableException:
        assert True


def test_compare_unknown_unknown():
    unknown_type_column_01 = YetUnknownTypeColumn('test unknown type column 1')
    unknown_type_column_02 = YetUnknownTypeColumn('test unknown type column 2')

    try:
        unknown_type_column_01 - unknown_type_column_02
        assert False
    except UncomparableException:
        assert True
