import pandas
import pytest
import sys

sys.path.insert(0, 'src')

from TFG_Seleccion_de_Vuelos.df_utilities import constants as const

column_name = 'col1'
reference_column_name = 'col2'
replaced_string = 'replaced string'

@pytest.fixture
def df():
    df = pandas.DataFrame({
        column_name: ['a', 'a', 'a'],
        reference_column_name: ['ACE', 'LPA', 'ELSE'],
        'col3': ['c', 'c', 'c'],
        const.DF_DAY_COL_NAME:  ["04/02/2019", "05/02/2019", "06/02/1999"]
    })

    df[const.DF_DAY_COL_NAME] = pandas.to_datetime(df[const.DF_DAY_COL_NAME], format=const.DF_DATAFRAME_DAY_FORMAT)
    return df

@pytest.fixture
def json_data():
    return {
        # Values used to substitute rows
        const.KW_COL_NAME: column_name,
        const.KW_REF_COL_NAME: reference_column_name,
        const.KW_REF_COL_VALUES: [
            "ACE",
            "LPA",
            "SPC",
            "AMS"
        ],
        const.KW_REPL_VALUE: replaced_string,

        # Values used to get the minimun inteview sample
        "arrange": "Arrays",
        "sample_as_percentage": False,
        const.KW_PASS_BY_STRATUM: [
            60,
            1000,
            10000,
            25000,
            40000,
            60000
        ],
        const.KW_MIN_SAMPLE: [
            20,
            80,
            200,
            400,
            500,
            600,
            700
        ],

        # Values that indicate the available days
        const.KW_COLUMN_DAY_NAME: const.DF_DAY_COL_NAME,
        const.KW_DAY_FORMAT: "%d/%m/%Y",
        const.KW_AVAILABLE_DAYS: [
            "04/02/2019",
            "05/02/2019"
        ]
    }
