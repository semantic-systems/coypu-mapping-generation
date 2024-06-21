import pytest

import util.columninferencer as col_inferencer

import pandas as pd

from semanticlabeling.labeledcolumn import LabeledColumn, BooleanColumn, \
    DateTimeColumn, IntegerColumn, IDColumn, StringColumn, TextColumn, \
    CategoriesColumn, FloatColumn, WGS84LatitudeColumn, WGS84LongitudeColumn


DATE_TIME_SERIES = pd.Series(data=[
        pd.to_datetime('2005-01-13'),
        pd.to_datetime('2005-02-13'),
        pd.to_datetime('2004-03-13'),
        pd.to_datetime('2003-04-13'),
        pd.to_datetime('2002-05-13'),
        pd.to_datetime('2001-06-13'),
        pd.to_datetime('2000-07-13'),
    ])


# DateTimeColumn
def test_infer_date_time_column():
    column_name = 'test name'
    typed_column: LabeledColumn = col_inferencer.transform_series(
        series=DATE_TIME_SERIES,
        series_name=column_name
    )

    assert isinstance(typed_column, DateTimeColumn)
    assert typed_column.min_date_time == pd.to_datetime('2000-07-13')
    assert pd.to_datetime('2003-02-20 13:42:51') < \
           typed_column.mean_date_time < \
           pd.to_datetime('2003-02-20 13:42:52')
    assert typed_column.column_name == column_name


BOOL_SERIES = pd.Series(
    data=[True, False, True, False, False, False, True, True, False, False]
)


# BooleanColumn
def test_infer_bool_column():
    column_name = 'test bool column'
    typed_column: LabeledColumn = col_inferencer.transform_series(
        series=BOOL_SERIES,
        series_name=column_name
    )

    assert isinstance(typed_column, BooleanColumn)
    assert typed_column.portion_true == 0.4
    assert typed_column.portion_false == 0.6
    assert typed_column.column_name == column_name


INTEGER_SERIES_01 = pd.Series(data=[23, 42, 1, 2, 3, 4, 5, 8, 9, 13])


# IntegerColumn
def test_infer_integer_column_01():
    column_name = 'test integer column'
    typed_column: LabeledColumn = col_inferencer.transform_series(
        series=INTEGER_SERIES_01,
        series_name=column_name
    )

    assert isinstance(typed_column, IntegerColumn)
    assert typed_column.min_value == 1
    assert typed_column.max_value == 42
    assert typed_column.avg_value == 11.0
    assert typed_column.value_stddev == pytest.approx(12.05, 0.01)  # 12.049896265113654
    assert typed_column.column_name == column_name


INTEGER_SERIES_02 = pd.Series(data=['23', '42', '1', '2', '3', '4', '5', '8', '9', '13'])


# IntegerColumn
def test_infer_integer_column_02():
    column_name = 'test integer column'
    typed_column: LabeledColumn = col_inferencer.transform_series(
        series=INTEGER_SERIES_02,
        series_name=column_name
    )

    assert isinstance(typed_column, IntegerColumn)
    assert typed_column.min_value == 1
    assert typed_column.max_value == 42
    assert typed_column.avg_value == 11.0
    assert typed_column.value_stddev == pytest.approx(12.05, 0.01)  # 12.049896265113654
    assert typed_column.column_name == column_name


ID_SERIES_01 = pd.Series(
    data=[
        999, 1001, 1002, 1003, 1004, 1005, 1006, 1008, 1009, 1010,
        1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020,
        1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030,
        1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040
    ]
)


# IDColumn
def test_infer_id_column_01():
    column_name = 'test ID column'
    typed_column: LabeledColumn = col_inferencer.transform_series(
        series=ID_SERIES_01,
        series_name=column_name
    )

    assert isinstance(typed_column, IDColumn)
    assert typed_column.min_id_length == 3
    assert typed_column.max_id_length == 4
    assert typed_column.avg_id_length == 3.975
    assert typed_column.column_name == column_name


ID_SERIES_02 = pd.Series(
    data=[
        '999', '1001', '1002', '1003', '1004', '1005', '1006', '1008', '1009',
        '1010', '1011', '1012', '1013', '1014', '1015', '1016', '1017', '1018',
        '1019', '1020', '1021', '1022', '1023', '1024', '1025', '1026', '1027',
        '1028', '1029', '1030', '1031', '1032', '1033', '1034', '1035', '1036',
        '1037', '1038', '1039', '1040'
    ]
)


# IDColumn
def test_infer_id_column_02():
    column_name = 'test 2 ID column'
    typed_column: LabeledColumn = col_inferencer.transform_series(
        series=ID_SERIES_02,
        series_name=column_name
    )

    assert isinstance(typed_column, IDColumn)
    assert typed_column.min_id_length == 3
    assert typed_column.max_id_length == 4
    assert typed_column.avg_id_length == 3.975
    assert typed_column.column_name == column_name


ID_SERIES_03 = pd.Series(
    data=[
        'ABC999X', 'U13A', 'ABC1002X', 'ABC1003X', 'ABC1004X', 'ABC1005X',
        'ABC1006X', 'ABC1008X', 'ABC1009X', 'ABC1010X', 'ABC1011X', 'ABC1012X',
        'ABC1013X', 'ABC1014X', 'ABC1015X', 'ABC1016X', 'ABC1017X', 'ABC1018X',
        'ABC1019X', 'ABC1020X', 'ABC1021X', 'ABC1022X', 'ABC1023X', 'ABC1024X',
        'ABC1025X', 'ABC1026X', 'ABC1027X', 'ABC1028X', 'ABC1029X', 'ABC1030X',
        'ABC1031X', 'ABC1032X', 'ABC1033X', 'ABC1034X', 'ABC1035X', 'ABC1036X',
        'ABC1037X', 'ABC1038X', 'ABC1039X', 'ABC1040X', 'ABC1041X', 'ABC1042X',
        'ABC1043X', 'ABC1044X', 'ABC1045X', 'ABC1046X', 'ABC1047X', 'ABC1048X',
        'ABC1049X', 'ABC1050X', 'ABC1051X', 'ABC1052X', 'ABC1053X', 'ABC1054X',
        'ABC1055X', 'ABC1056X', 'ABC1057X', 'ABC1058X', 'ABC1059X', 'ABC1060X',
        'ABC1061X', 'ABC1062X', 'ABC1063X', 'ABC1064X', 'ABC1065X', 'ABC1066X',
        'ABC1067X', 'ABC1068X', 'ABC1069X', 'ABC1070X'
    ]
)


# IDColumn
def test_infer_id_column_03():
    column_name = 'test 3 ID column'
    typed_column: LabeledColumn = col_inferencer.transform_series(
        series=ID_SERIES_03,
        series_name=column_name
    )

    assert isinstance(typed_column, IDColumn)
    assert typed_column.min_id_length == 4
    assert typed_column.max_id_length == 8
    assert typed_column.avg_id_length == pytest.approx(7.928, 0.01)  # 7.928571428571429
    assert typed_column.column_name == column_name


STR_SERIES = pd.Series(
    data=[
        'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
        'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
        'seventeen', 'eighteen', 'twenty'
    ]
)


# StringColumn
def test_infer_str_column():
    column_name = 'test string column'
    typed_column: LabeledColumn = col_inferencer.transform_series(
        series=STR_SERIES,
        series_name=column_name
    )

    assert isinstance(typed_column, StringColumn)
    assert typed_column.min_str_length == 3
    assert typed_column.max_str_length == 9
    assert typed_column.avg_str_length == pytest.approx(5.473, 0.01)  # 5.473684210526316
    assert typed_column.column_name == column_name


TEXT_SERIES = pd.Series(
    data=[
        'one is a number', 'two is a number', 'three', 'four is a number',
        'five as well', 'six is a number', 'seven is a number',
        'eight is a number', 'nine is a number', 'ten is a number',
        'eleven is a number as well', 'twelve is a number',
        'thirteen is a number', 'fourteen seems to be a number as well',
        'fifteen is a number'
    ]
)


# TextColumn
def test_infer_text_column():
    column_name = 'test text column'
    typed_column: LabeledColumn = col_inferencer.transform_series(
        series=TEXT_SERIES,
        series_name=column_name
    )

    assert isinstance(typed_column, TextColumn)
    assert typed_column.min_text_length == 5
    assert typed_column.max_text_length == 37
    assert typed_column.avg_text_length == pytest.approx(17.533, 0.01)  # 17.533333333333335
    assert typed_column.column_name == column_name


CATEGORY_SERIES = pd.Series(
    data=[
        'mammal', 'mammal', 'fish', 'bird', 'mammal', 'bird', 'bird', 'fish',
        'mammal', 'bird', 'mammal', 'fish', 'fish', 'mammal', 'bird', 'bird',
        'fish', 'bird', 'fish', 'fish', 'mammal', 'fish', 'bird', 'fish',
        'fish', 'mammal', 'fish', 'bird', 'bird', 'mammal', 'bird'
    ]
)


# CategoriesColumn
def test_infer_category_column():
    column_name = 'test category column'
    typed_column: LabeledColumn = col_inferencer.transform_series(
        series=CATEGORY_SERIES,
        series_name=column_name
    )

    assert isinstance(typed_column, CategoriesColumn)
    assert 'bird' in typed_column.categories
    assert 'fish' in typed_column.categories
    assert 'mammal' in typed_column.categories
    assert len(typed_column.categories) == 3
    assert typed_column.column_name == column_name


FLOAT_SERIES_01 = pd.Series(
    data=[
        0.136, 0.246, 0.372, 0.600, 0.154, 0.373, 0.316, 0.744, 0.129, 0.634,
        0.361, 0.789, 0.993, 0.035, 0.006, 0.909, 0.290, 0.677, 0.122, 0.307
    ]
)


# FloatColumn
def test_infer_float_column_01():
    column_name = 'test float column'
    typed_column: LabeledColumn = col_inferencer.transform_series(
        series=FLOAT_SERIES_01,
        series_name=column_name
    )

    assert isinstance(typed_column, FloatColumn)
    assert typed_column.min_value == 0.006
    assert typed_column.max_value == 0.993
    assert typed_column.avg_value == pytest.approx(0.409, 0.01)  # 0.40965000000000007
    assert typed_column.value_stddev == pytest.approx(0.296, 0.01)  # 0.296821987233532
    assert typed_column.column_name == column_name


FLOAT_SERIES_02 = pd.Series(
    data=[
        '0.136', '0.246', '0.372', '0.600', '0.154', '0.373', '0.316', '0.744',
        '0.129', '0.634', '0.361', '0.789', '0.993', '0.035', '0.006', '0.909',
        '0.290', '0.677', '0.122', '0.307'
    ]
)


# FloatColumn
def test_infer_float_column_02():
    column_name = 'test float column'
    typed_column: LabeledColumn = col_inferencer.transform_series(
        series=FLOAT_SERIES_02,
        series_name=column_name
    )

    assert isinstance(typed_column, FloatColumn)
    assert typed_column.min_value == 0.006
    assert typed_column.max_value == 0.993
    assert typed_column.avg_value == pytest.approx(0.409, 0.01)  # 0.40965000000000007
    assert typed_column.value_stddev == pytest.approx(0.296, 0.01)  # 0.296821987233532
    assert typed_column.column_name == column_name


LAT_SERIES = pd.Series(
    data=[
        35.6897, -6.1750, 28.6100, 23.1300, 19.0761, 14.5958, 31.2286,
        -23.5500, 37.5600, 19.4333, 30.0444, 40.6943, 23.7639, 39.9067,
        22.5675, 13.7525, 22.5415, 55.7558, -34.6033, 6.4550, 41.0136,
        24.8600, 12.9789, 10.7756, 34.6939, 30.6600, 35.6892, -4.3219,
        -22.9111, 13.0825, 34.2611, 31.5497, 29.5637, 34.1141, 38.8740,
        51.5072, 48.8567, 35.1038, 23.0210, 17.3617, 39.1336, -12.0600,
        30.5934, 32.9987, 30.2670, 23.0214, 35.1833, 34.2040, -8.8383,
        33.6250, 25.8310, 3.1478, 35.2343, 24.8744, -26.2044, 41.8375,
        32.0608, 35.4151, 21.0000, 18.5203, 32.8900, 23.0225, 4.7111, 41.8025,
        -6.8161, 15.6000, 34.4150, 22.3000, 38.3047, 24.6333, -33.4372, 37.0717,
        33.0140, 22.3350, -7.2458, 21.2701, 27.2840, 33.3482, 26.8940, 27.7220,
        27.2395, 21.1702, 28.4551, 32.1490, 40.4169, 33.3153
    ]
)


# WGS84LatitudeColumn
def test_infer_lat_column():
    column_name = 'test coord column'
    typed_column: LabeledColumn = col_inferencer.transform_series(
        series=LAT_SERIES,
        series_name=column_name
    )

    assert isinstance(typed_column, WGS84LatitudeColumn)
    assert typed_column.min_value == -34.6033
    assert typed_column.max_value == 55.7558
    assert typed_column.avg_value == pytest.approx(22.940, 0.01)  # 22.94093488372093
    assert typed_column.value_stddev == pytest.approx(18.485, 0.01)  # 18.487510222619882
    assert typed_column.column_name == column_name


LON_SERIES = pd.Series(
    data=[
        139.6922, 106.8275, 77.2300, 113.2600, 72.8775, 120.9772, 121.4747,
        -46.6333, 126.9900, -99.1333, 31.2358, -73.9249, 90.3889, 116.3975,
        88.3700, 100.4942, 114.0596, 37.6172, -58.3817, 3.3841, 28.9550,
        67.0100, 77.5917, 106.7019, 135.5022, 104.0633, 51.3889, 15.3119,
        -43.2056, 80.2750, 108.9422, 74.3436, 106.5504, -118.4068, 115.4640,
        -0.1275, 2.3522, 118.3564, 113.7520, 78.4747, 117.2054, -77.0375,
        114.3046, 112.5292, 120.1530, 113.1216, 136.9000, 117.2840, 13.2344,
        114.6418, 114.9330, 101.6953, 115.4796, 118.6757, 28.0456, -87.6866,
        118.7789, 116.5871, 105.8500, 73.8567, 115.8140, 72.5714, -74.0722,
        123.4281, 39.2803, 32.5000, 115.6560, 114.2000, 116.8387, 46.7167,
        -70.6506, 114.5048, 114.0220, 91.8325, 112.7378, 110.3575, 105.2920,
        120.1626, 112.5720, 107.0310, 111.4679, 72.8311, 117.9431, 114.0910
    ]
)


# WGS84LongitudeColumn
def test_infer_lon_column():
    column_name = 'test coord column'
    typed_column: LabeledColumn = col_inferencer.transform_series(
        series=LON_SERIES,
        series_name=column_name
    )

    assert isinstance(typed_column, WGS84LongitudeColumn)
    assert typed_column.min_value == -118.4068
    assert typed_column.max_value == 139.6922
    assert typed_column.avg_value == pytest.approx(73.002, 0.01)  # 73.00212142857144
    assert typed_column.value_stddev == pytest.approx(64.599, 0.01)  # 64.59929679189058
    assert typed_column.column_name == column_name
