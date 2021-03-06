"""General purpose functions
"""

import sys


def flatten(list_of_lists: list) -> list:
    """Helper function to flat a list out of lists

    Args:
        list_of_lists (list): [description]

    Returns:
        list: [description]
    """
    flat_list = []
    for sublist in list_of_lists:
        for item in sublist:
            flat_list.append(item)
    return flat_list


def path_modules():
    """Helper function that prints the modules of the current environment
    """
    import sys
    for file in sys.path:
        print(file)


def eprint(*args, **kwargs):
    """Method that handles error messages
    """
    print(*args, file=sys.stderr, **kwargs)
