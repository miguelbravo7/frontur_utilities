import pandas
import re
import json
import df_utilities.constants as const
import df_utilities.utility_fileloader as df_fileloader
import df_utilities.utility_df_datetime as df_datetime
import df_utilities.utility_functions as utility
import df_utilities.utility_df as df_utility


def select_airport(
        data_frame: pandas.DataFrame,
        airport: str,
        target_col: str = const.DF_ORIGIN_COL_NAME
        ) -> pandas.DataFrame:
    """Selects rows by the airport code

    Args:
        data_frame (pandas.DataFrame): Source DataFrame
        airport (str): String code of the airport
        target_col (str): Target column

    Returns:
        pandas.DataFrame: Selected airport entries
    """
    data_frame = data_frame.loc[lambda frame: frame[target_col] == airport]
    if data_frame.empty:
        utility.eprint(f'Selected airport "{airport}" is invalid or not found.')
        return
    return data_frame


def substitute_values(df: pandas.DataFrame, file_path: str):
    """Substitutes DataFrame values given a dictionary

    Args:
        df (pandas.DataFrame): Source DataFrame
        file_path (str): Source file path
    """
    with open(file_path) as jfile:
        df_utility.substitute_rows(df, json.load(jfile))


def add_plane_data(
        data_frame: pandas.DataFrame,
        file_path: str,
        target_col: str = const.DF_PLANE_COL_NAME
        ) -> pandas.DataFrame:
    """Merges DataFrame with information about the flight planes

    Args:
        data_frame (pandas.DataFrame): Source DataFrame
        file_path (str): Source file path
        target_col (str): Target column to merge

    Returns:
        pandas.DataFrame: Source DataFrame with aditional information
    """
    planes = df_fileloader.load_agenda(file_path)
    data_frame[target_col] = data_frame[target_col].astype(str)
    planes[target_col] = planes[target_col].astype(str)
    data_frame = pandas.merge(data_frame, planes, how='outer', on=[target_col], indicator=True)
    unmatched = data_frame.query('_merge == "left_only"').groupby([target_col]).size().reset_index(name='count')
    if not unmatched.empty:
        err_msg = 'There\'s missing information about the following planes:'
        for index, row in unmatched.iterrows():
            err_msg += '\n {} with {} ocurrences.'.format(row[target_col], row['count'])
        utility.eprint(err_msg)
        return
    return data_frame.query('_merge == "both"').drop(columns=['_merge'])


def format_dates(
    data_frame: pandas.DataFrame,
    target_col: str = const.DF_WEEKDAY_COL_NAME
    ) -> pandas.DataFrame:
    """Removes all whitespaces from the deafult date column

    Args:
        data_frame (pandas.DataFrame): source DataFrame
        target_col (str): Target column

    Returns:
        pandas.DataFrame: Manipulated DataFrame
    """
    data_frame[target_col] = data_frame.apply(lambda row: re.sub(r"\s+", '', row[target_col]), axis='columns')
    dict_lists = data_frame.apply(lambda row: df_datetime.expand_date_intervals(row), axis='columns')
    return pandas.pandas.DataFrame(utility.flatten(dict_lists))


def select_days(df: pandas.DataFrame, file_path: str) -> pandas.DataFrame:
    """Selects rows using a json file with specific parameters

    Args:
        df (pandas.DataFrame): Source DataFrame
        file_path (str): Source file path

    Returns:
        pandas.DataFrame: DataFrame with the selected values
    """
    with open(file_path) as jfile:
        return df_utility.select_rows(df, json.load(jfile))
