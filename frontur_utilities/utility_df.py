"""Methods that deal with data manipulation and selection
"""

import frontur_utilities.utility_df_datetime as df_datetime
import frontur_utilities.constants as const
from bisect import bisect
import pandas


def replace_value(
        row: dict,
        trad_dict: dict,
        json_column_name: str = const.KW_COL_NAME,
        json_reference_column_name: str = const.KW_REF_COL_NAME,
        json_reference_column_values: str = const.KW_REF_COL_VALUES,
        json_replace_value: str = const.KW_REPL_VALUE
        ) -> any:
    """Helper function to replace a value given a dictionary
    if not found in the dictionary

    Args:
        row (dict): Source DataFrame row
        trad_dict (dict): Dictionary with the parameters required to do the map operation
        json_column_name (str, optional): Parameter key to the target column name.
        json_reference_column_name (str, optional): Parameter key to the target column value to be compared.
        json_reference_column_values (str, optional): Parameter key to a list of searched values.
        json_replace_value (str, optional): Parameter key to the replace value.

    Returns:
        str: Either the original or replaced value
    """
    if row[trad_dict[json_reference_column_name]] in trad_dict[json_reference_column_values]:
        return trad_dict[json_replace_value]
    else:
        return row[trad_dict[json_column_name]]


def minimum_sample(
        number_of_passengers: int,
        json_data: dict,
        pass_by_stratum: str = const.KW_PASS_BY_STRATUM,
        min_sample: str = const.KW_MIN_SAMPLE
        ) -> int:
    """Helper function that returns the minimum sample of people to interview

    Args:
        number_of_passengers (int): Actual number of passengers
        json_data (dict): Dictionary with the parameters required to do the map operation
        pass_by_stratum (str, optional): Parameter key to the value that indicates the stratum of passenger.
        min_sample (str, optional): Parameter key to minimum required sample.

    Returns:
        int: Minimum number of required polls
    """
    pos = bisect(json_data[pass_by_stratum], number_of_passengers)
    return json_data[min_sample][pos]


def select_rows(
        data_frame: pandas.DataFrame,
        json_data: dict,
        date_format: str = const.KW_DAY_FORMAT,
        available_days: str = const.KW_AVAILABLE_DAYS,
        column_name: str = const.KW_COLUMN_DAY_NAME,
        alt_format: str = "",
        days: list = []
        ) -> pandas.DataFrame:
    """Function that selects rows by a given dictionary
    with the available days

    Args:
        data_frame (pandas.DataFrame): Source DataFrame
        json_data (dict): Dictionary with the parameters required to do the map operation
        date_format (str, optional): Parameter key to the date format.
        available_days (str, optional): Parameter key to the available days.
        column_name (str, optional): Parameter key to the source column.
        alt_format (str, optional): Alternative date format.
        days (list, optional): List of dates that are going to be searched.

    Returns:
        pandas.DataFrame: DataFrame with the selected dates
    """
    if not days:
        if(alt_format == ""):
            alt_format = json_data[date_format]
        days = frozenset(df_datetime.conv_to_datetime(json_data[available_days], alt_format))
    return data_frame.loc[data_frame[json_data[column_name]].isin(days)]


def substitute_rows(
        data_frame: pandas.DataFrame,
        json_data: dict,
        json_column_name: str = const.KW_COL_NAME,
        json_reference_column_name: str = const.KW_REF_COL_NAME,
        json_reference_column_values: str = const.KW_REF_COL_VALUES,
        json_replace_value: str = const.KW_REPL_VALUE
        ):
    """Substitutes the values of a column given a dictionary

    Args:
        data_frame (pandas.DataFrame): [Source DataFrame]
        json_data (dict): Dictionary with the parameters required to do the map operation
        json_column_name (str, optional): Parameter key to the target column name.
        json_reference_column_name (str, optional): Parameter key to the reference column name.
        json_reference_column_values (str, optional): Parameter key to the reference column values that are searched.
        json_replace_value (str, optional): Parameter key to the replace value.
    """
    if not isinstance(json_data, list):
        json_data = [json_data]

    for substitution_map in json_data:
        data_frame[substitution_map[json_column_name]] = data_frame.apply(
            lambda row: replace_value(
                row,
                substitution_map,
                json_column_name=json_column_name,
                json_reference_column_name=json_reference_column_name,
                json_reference_column_values=json_reference_column_values,
                json_replace_value=json_replace_value
                ),
            axis='columns')
