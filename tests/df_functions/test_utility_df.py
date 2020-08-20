import pandas
import sys

sys.path.insert(0, 'src')
sys.path.insert(0, 'tests')

from df_utilities import utility_df, constants as const
from fixtures import df, json_data


def test_replace_value(df, json_data):
    # Assertions use Dataframe instances of only one row
    dict_arr = df.to_dict(orient='records') 
    
    # Check when the values should be substituted
    assert json_data[const.KW_REPL_VALUE] == utility_df.replace_value(dict_arr[0], json_data)
    assert json_data[const.KW_REPL_VALUE] == utility_df.replace_value(dict_arr[1], json_data)

    # Check when the values should not be substituted
    assert dict_arr[2][json_data[const.KW_COL_NAME]] == utility_df.replace_value(dict_arr[2], json_data)
    

def test_minimum_sample(json_data):
    # Left edge cases
    assert json_data[const.KW_MIN_SAMPLE][1] == utility_df.minimum_sample(json_data[const.KW_PASS_BY_STRATUM][0] + 1, json_data)
    assert json_data[const.KW_MIN_SAMPLE][1] == utility_df.minimum_sample(json_data[const.KW_PASS_BY_STRATUM][0], json_data)
    assert json_data[const.KW_MIN_SAMPLE][0] == utility_df.minimum_sample(json_data[const.KW_PASS_BY_STRATUM][0] - 1, json_data)

    # Middle cases
    assert json_data[const.KW_MIN_SAMPLE][2] == utility_df.minimum_sample(json_data[const.KW_PASS_BY_STRATUM][1] + 1, json_data)
    assert json_data[const.KW_MIN_SAMPLE][2] == utility_df.minimum_sample(json_data[const.KW_PASS_BY_STRATUM][1], json_data)
    assert json_data[const.KW_MIN_SAMPLE][1] == utility_df.minimum_sample(json_data[const.KW_PASS_BY_STRATUM][1] - 1, json_data)

    # Right edge cases
    assert json_data[const.KW_MIN_SAMPLE][-1] == utility_df.minimum_sample(json_data[const.KW_PASS_BY_STRATUM][-1] + 1, json_data)
    assert json_data[const.KW_MIN_SAMPLE][-1] == utility_df.minimum_sample(json_data[const.KW_PASS_BY_STRATUM][-1], json_data)
    assert json_data[const.KW_MIN_SAMPLE][-2] == utility_df.minimum_sample(json_data[const.KW_PASS_BY_STRATUM][-1] - 1, json_data)



def test_select_rows(df, json_data):
    from datetime import datetime

    expected_df = pandas.DataFrame({
        'col1': ['a', 'a'],
        'col2': ['ACE', 'LPA'],
        'col3': ['c', 'c'],
        const.DF_DAY_COL_NAME:  ["04/02/2019", "05/02/2019"]
    })
    expected_df[const.DF_DAY_COL_NAME] = pandas.to_datetime(expected_df[const.DF_DAY_COL_NAME], format=const.DF_DATAFRAME_DAY_FORMAT)

    actual_df = utility_df.select_rows(df, json_data)
    
    pandas.testing.assert_frame_equal(actual_df, expected_df)

def test_substitute_rows(df):
    assert True