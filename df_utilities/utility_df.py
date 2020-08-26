import df_utilities.utility_df_datetime as df_datetime
import df_utilities.constants as const
from bisect import bisect
import pandas


def replace_value(
        value: str,
        trad_dict: dict,
        json_column_name: str = const.KW_COL_NAME,
        json_reference_column_name: str = const.KW_REF_COL_NAME,
        json_reference_column_values: str = const.KW_REF_COL_VALUES,
        json_replace_value: str = const.KW_REPL_VALUE
        ) -> str:
    """Helper function to replace a value given a dictionary
    if not found in the dictionary

    Args:
        value (str): [description]
        trad_dict (dict): [description]
        json_column_name (str, optional): [description]. Defaults to const.KW_COL_NAME.
        json_reference_column_name (str, optional): [description]. Defaults to const.KW_REF_COL_NAME.
        json_reference_column_values (str, optional): [description]. Defaults to const.KW_REF_COL_VALUES.
        json_replace_value (str, optional): [description]. Defaults to const.KW_REPL_VALUE.

    Returns:
        str: [description]
    """
    if value[trad_dict[json_reference_column_name]] in trad_dict[json_reference_column_values]:
        return trad_dict[json_replace_value] 
    else:
        return value[trad_dict[json_column_name]]


def minimum_sample(
        number_of_passengers: int,
        json_data: dict,
        pass_by_stratum: str = const.KW_PASS_BY_STRATUM,
        min_sample: str = const.KW_MIN_SAMPLE
        ) -> str:
    """Helper function that returns the minimum sample of people to interview

    Args:
        number_of_passengers (int): [description]
        json_data (dict): [description]
        pass_by_stratum (str, optional): [description]. Defaults to const.KW_PASS_BY_STRATUM.
        min_sample (str, optional): [description]. Defaults to const.KW_MIN_SAMPLE.

    Returns:
        str: [description]
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

    Args:
        data_frame (pandas.DataFrame): [description]
        json_data (dict): [description]
        date_format (str, optional): [description]. Defaults to const.KW_DAY_FORMAT.
        available_days (str, optional): [description]. Defaults to const.KW_AVAILABLE_DAYS.
        column_name (str, optional): [description]. Defaults to const.KW_COLUMN_DAY_NAME.
        alt_format (str, optional): [description]. Defaults to "".
        days (list, optional): [description]. Defaults to [].

    Returns:
        pandas.DataFrame: [description]
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
        data_frame (pandas.DataFrame): [description]
        json_data (dict): [description]
        json_column_name (str, optional): [description]. Defaults to const.KW_COL_NAME.
        json_reference_column_name (str, optional): [description]. Defaults to const.KW_REF_COL_NAME.
        json_reference_column_values (str, optional): [description]. Defaults to const.KW_REF_COL_VALUES.
        json_replace_value (str, optional): [description]. Defaults to const.KW_REPL_VALUE.
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
