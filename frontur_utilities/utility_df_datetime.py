"""Methods that operate on date logic and arithmetic
"""

from datetime import datetime, timedelta
from pandas import DataFrame
import frontur_utilities.constants as const


def conv_to_datetime(day_str_arr: list, day_format: str) -> list:
    """Given a string with a date and another with its format
    converts the string to ea datetime object

    Args:
        day_str_arr (list): List that contains the strings with the date formatted
        day_format (str): String that specifies the format of the day string

    Returns:
        list: List of datetime objects
    """
    dates = []
    for day in day_str_arr:
        dates.append(datetime.strptime(day, day_format))
    dates.sort()
    return dates


def parse_workdays(
        available_work_days: str,
        dictionary: dict = const.WEEKDAY
        ) -> list:
    """Parses a string to return an array of weekday numbers

    Args:
        available_work_days (str): A string of individual character workdays
        dictionary (dict, optional): Map of aliases to the characters.

    Returns:
        list: Integer list of the corresponding weekdays
    """
    work_days = []
    for value in available_work_days:
        work_days.append(dictionary[value])
    work_days.sort()
    return work_days


def next_date(date: datetime, day: int) -> datetime:
    """Gives the next datetime given date and the next chosen weekday

    Args:
        date (datetime): Start instance of time
        day (int): Weekday number to look after the given date

    Returns:
        datetime: Date found after the given start date
    """
    return date + timedelta(days=(day - date.weekday()) % 7)


def gen_dates(
        dt_first: datetime,
        dt_last: datetime,
        available_work_days: list
        ) -> datetime:
    """Gives the set of dates given the interval of the two dates
    and an array of available week day numbers

    Args:
        dt_first (datetime): Start date of tje interval
        dt_last (datetime): Last date of the interval
        available_work_days (list): list of workday integers

    Returns:
        datetime: set of possible datetimes between the given dates
    """
    dates = set()
    while True:
        tmp_dates = []
        for day in available_work_days:
            tmp_dates.append(next_date(dt_first, day))
        dt_first = dt_first + timedelta(weeks=1)
        tmp_dates.sort()
        if tmp_dates[-1] > dt_last:
            while (len(tmp_dates) > 0) and (tmp_dates[-1] > dt_last):
                tmp_dates.pop(-1)
            dates.update(tmp_dates)
            break
        dates.update(tmp_dates)
    return dates


def expand_date_intervals(
        df: DataFrame,
        week_days: str = const.DF_WEEKDAY_COL_NAME,
        start_row: str = const.DF_OPERATION_START_COL_NAME,
        end_row: str = const.DF_OPERATION_END_COL_NAME,
        day_name: str = const.DF_DAY_COL_NAME
        ) -> list:
    """Given a dataframe row multiple instances of single dates are made
    using a date interval and available weekdays

    Args:
        df (pandas.DataFrame): Source DataFrame
        week_days (str, optional): Name of the column that contains the workday characters.
        start_row (str, optional): Name of the column that contains the start date of opertation.
        end_row (str, optional): Name of the column that contains the last date of opertation.
        day_name (str, optional): Name of the generated column after the process.

    Returns:
        list: list of dictionaries
    """
    workdays = parse_workdays(df[week_days])
    generated_dates = gen_dates(df[start_row], df[end_row], workdays)
    rows_list = []
    dict1 = df.to_dict()
    dict1.pop(week_days, None)
    dict1.pop(start_row, None)
    dict1.pop(end_row, None)
    for date in generated_dates:
        rows_list.append(dict(dict1, **{day_name: date}))
    return rows_list
