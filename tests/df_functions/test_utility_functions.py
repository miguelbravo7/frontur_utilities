from df_utilities import utility_functions


def test_flatten():
    assert [3, 4, 1, 5, 2] == utility_functions.flatten([[3, 4], [1, 5, 2]])