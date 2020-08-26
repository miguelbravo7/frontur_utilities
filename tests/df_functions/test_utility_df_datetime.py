import pandas
from datetime import datetime
from df_utilities import df_datetime, constants as const


def test_conv_to_datetime():
    expected = [
        datetime.strptime("04/02/2019", const.DF_DATAFRAME_DAY_FORMAT),
        datetime.strptime("05/02/2019", const.DF_DATAFRAME_DAY_FORMAT)
        ]
    actual = df_datetime.conv_to_datetime(["04/02/2019", "05/02/2019"], const.DF_DATAFRAME_DAY_FORMAT)

    assert expected == actual


def test_parse_workdays():
    assert [0] == df_datetime.parse_workdays('L')
    assert [1] == df_datetime.parse_workdays('M')
    assert [2] == df_datetime.parse_workdays('X')
    assert [3] == df_datetime.parse_workdays('J')
    assert [4] == df_datetime.parse_workdays('V')
    assert [5] == df_datetime.parse_workdays('S')
    assert [6] == df_datetime.parse_workdays('D')
    assert [0, 1, 2, 3, 4] == df_datetime.parse_workdays('LMXJV')
    assert [2, 4] == df_datetime.parse_workdays('XV')
    assert [0, 3, 4, 5, 6] == df_datetime.parse_workdays('LSDJV')


def test_next_date():
    monday = datetime.strptime("23/03/2020", const.DF_DATAFRAME_DAY_FORMAT)

    assert datetime.strptime("23/03/2020", const.DF_DATAFRAME_DAY_FORMAT) == df_datetime.next_date(monday, 0)
    assert datetime.strptime("24/03/2020", const.DF_DATAFRAME_DAY_FORMAT) == df_datetime.next_date(monday, 1)
    assert datetime.strptime("25/03/2020", const.DF_DATAFRAME_DAY_FORMAT) == df_datetime.next_date(monday, 2)
    assert datetime.strptime("26/03/2020", const.DF_DATAFRAME_DAY_FORMAT) == df_datetime.next_date(monday, 3)
    assert datetime.strptime("27/03/2020", const.DF_DATAFRAME_DAY_FORMAT) == df_datetime.next_date(monday, 4)
    assert datetime.strptime("28/03/2020", const.DF_DATAFRAME_DAY_FORMAT) == df_datetime.next_date(monday, 5)
    assert datetime.strptime("29/03/2020", const.DF_DATAFRAME_DAY_FORMAT) == df_datetime.next_date(monday, 6)


def test_gen_dates():
    left_interval = datetime.strptime("23/03/2020", const.DF_DATAFRAME_DAY_FORMAT)
    right_interval = datetime.strptime("30/03/2020", const.DF_DATAFRAME_DAY_FORMAT)

    expected = set(map(lambda x: datetime.strptime(x, const.DF_DATAFRAME_DAY_FORMAT),[
        "23/03/2020", 
        "24/03/2020", 
        "25/03/2020", 
        "26/03/2020", 
        "27/03/2020", 
        "28/03/2020", 
        "29/03/2020", 
        "30/03/2020", 
    ]))

    actual = df_datetime.gen_dates(left_interval, right_interval, [0, 1, 2, 3, 4, 5, 6])

    assert expected == actual

    left_interval = datetime.strptime("16/03/2020", const.DF_DATAFRAME_DAY_FORMAT)
    right_interval = datetime.strptime("30/03/2020", const.DF_DATAFRAME_DAY_FORMAT)

    expected = set(map(lambda x: datetime.strptime(x, const.DF_DATAFRAME_DAY_FORMAT),[
        "16/03/2020", 
        "23/03/2020", 
        "30/03/2020", 
    ]))

    actual = df_datetime.gen_dates(left_interval, right_interval, [0])

    assert expected == actual

    left_interval = datetime.strptime("21/03/2020", const.DF_DATAFRAME_DAY_FORMAT)
    right_interval = datetime.strptime("06/04/2020", const.DF_DATAFRAME_DAY_FORMAT)

    expected = set(map(lambda x: datetime.strptime(x, const.DF_DATAFRAME_DAY_FORMAT),[
        "22/03/2020", 
        "29/03/2020", 
        "05/04/2020", 
    ]))

    actual = df_datetime.gen_dates(left_interval, right_interval, [6])

    assert expected == actual


def test_expand_date_intervals():
    data_frame = pandas.DataFrame({
        const.DF_WEEKDAY_COL_NAME: ['M'],
        const.DF_OPERATION_START_COL_NAME: [datetime.strptime("23/03/2020", const.DF_DATAFRAME_DAY_FORMAT)],
        const.DF_OPERATION_END_COL_NAME: [datetime.strptime("30/03/2020", const.DF_DATAFRAME_DAY_FORMAT)]
    })

    expected = [{const.DF_DAY_COL_NAME: datetime.strptime("24/03/2020", const.DF_DATAFRAME_DAY_FORMAT)}]

    assert expected == df_datetime.expand_date_intervals(data_frame.iloc[0])
