from pandas import pandas
import re
import json
import df_utilities.constants as const
import df_utilities.utility_fileloader as df_fileloader
import df_utilities.utility_df_datetime as df_datetime
import df_utilities.utility_functions as utility
import df_utilities.utility_df as df_utility


def select_airport(data_frame, airport):
    data_frame = data_frame.loc[lambda frame: frame[const.DF_ORIGIN_COL_NAME] == airport]
    if data_frame.empty:
        utility.eprint(f'Selected airport "{airport}" is invalid or not found.')
        return
    return data_frame


def substitute_values(df, file_path):
    with open(file_path) as jfile:
        df_utility.substitute_rows(df, json.load(jfile))


def add_plane_data(data_frame, file_path):
    planes = df_fileloader.load_agenda(file_path)
    data_frame[const.DF_PLANE_COL_NAME] = data_frame[const.DF_PLANE_COL_NAME].astype(str)
    planes[const.DF_PLANE_COL_NAME] = planes[const.DF_PLANE_COL_NAME].astype(str)
    data_frame = pandas.merge(data_frame, planes, how='outer', on=[const.DF_PLANE_COL_NAME], indicator=True)
    unmatched = data_frame.query('_merge == "left_only"').groupby(["Aeronave"]).size().reset_index(name='count')
    if not unmatched.empty:
        err_msg = 'There\'s missing information about the following planes:'
        for index, row in unmatched.iterrows():
            err_msg += '\n {} with {} ocurrences.'.format(row[const.DF_PLANE_COL_NAME], row['count'])
        utility.eprint(err_msg)
        return
    return data_frame.query('_merge == "both"').drop(columns=['_merge'])


def format_dates(data_frame):
    data_frame[const.DF_WEEKDAY_COL_NAME] = data_frame.apply(lambda row: re.sub(r"\s+", '', row[const.DF_WEEKDAY_COL_NAME]), axis='columns')
    dict_lists = data_frame.apply(lambda row: df_datetime.expand_date_intervals(row), axis='columns')
    return pandas.DataFrame(utility.flatten(dict_lists))


def select_days(df, file_path):        
    with open(file_path) as jfile:
        return df_utility.select_rows(df, json.load(jfile))
