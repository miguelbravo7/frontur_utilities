import pandas
import pytest
from datetime import datetime
from df_utilities import df_datetime, constants as const


def test_conv_to_datetime():
    expected = [
        datetime.strptime("04/02/2019", const.DF_DATAFRAME_DAY_FORMAT),
        datetime.strptime("05/02/2019", const.DF_DATAFRAME_DAY_FORMAT)
        ]
    actual = df_datetime.conv_to_datetime(["04/02/2019", "05/02/2019"], const.DF_DATAFRAME_DAY_FORMAT)

    assert expected == actual

@pytest.mark.parametrize('expected, value', [
    ([0], 'L'),
    ([1], 'M'),
    ([2], 'X'),
    ([3], 'J'),
    ([4], 'V'),
    ([5], 'S'),
    ([6], 'D'),
    ([0, 1, 2, 3, 4], 'LMXJV'),
    ([2, 4], 'XV'),
    ([0, 3, 4, 5, 6], 'LSDJV')
])
def test_parse_workdays(expected, value):
    assert expected == df_datetime.parse_workdays(value)


def test_next_date():
    monday = datetime.strptime("23/03/2020", const.DF_DATAFRAME_DAY_FORMAT)

    assert datetime.strptime("23/03/2020", const.DF_DATAFRAME_DAY_FORMAT) == df_datetime.next_date(monday, 0)
    assert datetime.strptime("24/03/2020", const.DF_DATAFRAME_DAY_FORMAT) == df_datetime.next_date(monday, 1)
    assert datetime.strptime("25/03/2020", const.DF_DATAFRAME_DAY_FORMAT) == df_datetime.next_date(monday, 2)
    assert datetime.strptime("26/03/2020", const.DF_DATAFRAME_DAY_FORMAT) == df_datetime.next_date(monday, 3)
    assert datetime.strptime("27/03/2020", const.DF_DATAFRAME_DAY_FORMAT) == df_datetime.next_date(monday, 4)
    assert datetime.strptime("28/03/2020", const.DF_DATAFRAME_DAY_FORMAT) == df_datetime.next_date(monday, 5)
    assert datetime.strptime("29/03/2020", const.DF_DATAFRAME_DAY_FORMAT) == df_datetime.next_date(monday, 6)

@pytest.mark.parametrize('first_date, last_date, expected_dates, workdays', [
    ("23/03/2020", "30/03/2020", [
        "23/03/2020",
        "24/03/2020",
        "25/03/2020",
        "26/03/2020",
        "27/03/2020",
        "28/03/2020",
        "29/03/2020",
        "30/03/2020",
    ], [0, 1, 2, 3, 4, 5, 6]),
    ("16/03/2020", "30/03/2020", [
        "16/03/2020", 
        "23/03/2020", 
        "30/03/2020", 
    ], [0]),
    ("21/03/2020", "06/04/2020", [
        "22/03/2020", 
        "29/03/2020", 
        "05/04/2020", 
    ], [6])
])
def test_gen_dates(first_date, last_date, expected_dates, workdays):
    left_interval = datetime.strptime(first_date, const.DF_DATAFRAME_DAY_FORMAT)
    right_interval = datetime.strptime(last_date, const.DF_DATAFRAME_DAY_FORMAT)

    expected = set(map(lambda x: datetime.strptime(x, const.DF_DATAFRAME_DAY_FORMAT), expected_dates))

    actual = df_datetime.gen_dates(left_interval, right_interval, workdays)

    assert expected == actual


def test_expand_date_intervals():
    data_frame = pandas.DataFrame({
        const.DF_WEEKDAY_COL_NAME: ['M'],
        const.DF_OPERATION_START_COL_NAME: [datetime.strptime("23/03/2020", const.DF_DATAFRAME_DAY_FORMAT)],
        const.DF_OPERATION_END_COL_NAME: [datetime.strptime("30/03/2020", const.DF_DATAFRAME_DAY_FORMAT)]
    })

    expected = [{const.DF_DAY_COL_NAME: datetime.strptime("24/03/2020", const.DF_DATAFRAME_DAY_FORMAT)}]

    assert expected == df_datetime.expand_date_intervals(data_frame.iloc[0])
