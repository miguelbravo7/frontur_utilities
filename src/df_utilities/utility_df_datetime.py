from datetime import datetime, timedelta
import df_utilities.constants as const


def conv_to_datetime(day_str_arr, day_format):
    """
    Given a string with a date and another with its format
    converts the string to a datetime object

    Parameters
    ----------
    day_str_arr: list
        list that contain the strings with the date formatted
    day_format: string
        string that specifies the format of the day string

    Returns
    -------
    list of datetime objects
    """
    dates = []
    for day in day_str_arr:
        dates.append(datetime.strptime(day, day_format))
    dates.sort()
    return dates


def parse_workdays(available_work_days, dictionary=const.WEEKDAY):
    """
    Parses a string to return an array of weekday numbers

    Parameters
    ----------
    available_work_days: string

    Returns
    -------
    int list
    """
    work_days = []
    for value in available_work_days:
        work_days.append(dictionary[value])
    work_days.sort()
    return work_days


def next_date(date, day):
    """
    Gives the next datetime given date and the next chosen weekday

    Parameters
    ----------
    date: datetime object
    day: int

    Returns
    -------
    datetime object
    """
    return date + timedelta(days= (day - date.weekday()) % 7)


def gen_dates(dt_first, dt_last, available_work_days):
    """
    Gives the set of dates given the interval of the two dates
    and an array of available week day numbers

    Parameters
    ----------
    dt_first: datetime object
    dt_last: datetime object
    available_work_days: list of integers

    Returns
    -------
    datetime object set
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
        df,
        week_days=const.DF_WEEKDAY_COL_NAME, 
        start_row=const.DF_OPERATION_START_COL_NAME, 
        end_row=const.DF_OPERATION_END_COL_NAME,
        day_name=const.DF_DAY_COL_NAME
        ):
    """
    Given a dataframe row multiple instances of single dates are made
    using a date interval and available weekdays

    Parameters
    ----------
    df: pandas DateFrame object
    week_days: string, optional
    start_row: string, optional
    end_row: string, optional
    day_name: string, optional

    Returns
    -------
    list of dictionaries

    See Also
    --------
    parse_workdays
    gen_dates
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
