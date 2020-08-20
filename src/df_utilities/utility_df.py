import df_utilities.utility_df_datetime as df_datetime
import df_utilities.constants as const
from bisect import bisect


def replace_value(value,
                  trad_dict,
                  json_column_name=const.KW_COL_NAME,
                  json_reference_column_name=const.KW_REF_COL_NAME,
                  json_reference_column_values=const.KW_REF_COL_VALUES,
                  json_replace_value=const.KW_REPL_VALUE):
    """
    Helper function to replace a value given a dictionary
    if not found in the dictionary

    Parameters
    ----------
    value: string
    trad_dict: 

    Returns
    -------
    string
    """
    return trad_dict[json_replace_value] if value[trad_dict[json_reference_column_name]] in trad_dict[json_reference_column_values] else value[trad_dict[json_column_name]]


def minimum_sample(number_of_passengers,
                   json_data,
                   pass_by_stratum=const.KW_PASS_BY_STRATUM,
                   min_sample=const.KW_MIN_SAMPLE
                   ):
    """
    Helper function to give the minimum sample of people to interview

    Parameters
    ----------
    number_of_passengers: int
    json_data: dictionary

    Returns
    -------
    string
    """
    pos = bisect(json_data[pass_by_stratum], number_of_passengers)
    return json_data[min_sample][pos]


def select_rows(data_frame,
                json_data,
                date_format=const.KW_DAY_FORMAT,
                available_days=const.KW_AVAILABLE_DAYS,
                column_name=const.KW_COLUMN_DAY_NAME,
                format="",
                days=[]):
    """
    Function that selects rows by a given dictionary

    Parameters
    ----------
    data_frame: pandas DataFrame object
    json_data: dictionary

    Returns
    -------
    pandas DataFrame object
    """
    if not days:
        if(format == ""):
            format = json_data[date_format]
        days = frozenset(df_datetime.conv_to_datetime(json_data[available_days], format))
    return data_frame.loc[data_frame[json_data[column_name]].isin(days)]


def substitute_rows(data_frame,
                    json_data,
                    json_column_name=const.KW_COL_NAME,
                    json_reference_column_name=const.KW_REF_COL_NAME,
                    json_reference_column_values=const.KW_REF_COL_VALUES,
                    json_replace_value=const.KW_REPL_VALUE):
    """
    Substitutes the values of a column given a dictionary

    Parameters
    ----------
    data_frame: pandas DataFrame object
    json_data: dictionary

    See Also
    --------
    replace_value
    """
    if not isinstance(json_data, list):
        json_data = [json_data]

    for substitution_map in json_data:
        data_frame[substitution_map[json_column_name]] = data_frame.apply(
            lambda row: replace_value(row,
                                      substitution_map,
                                      json_column_name=json_column_name,
                                      json_reference_column_name=json_reference_column_name,
                                      json_reference_column_values=json_reference_column_values,
                                      json_replace_value=json_replace_value
                                    ),
            axis='columns')
