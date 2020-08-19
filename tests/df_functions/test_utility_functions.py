import pandas 
import pytest
import sys

sys.path.insert(0, 'src')

from df_utilities import utility_functions, constants as const

def test_flatten():
    assert [3, 4, 1, 5, 2] == utility_functions.flatten([[3, 4], [1, 5, 2]])