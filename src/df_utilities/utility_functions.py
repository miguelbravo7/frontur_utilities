import sys


def flatten(list_of_lists):
    """
    Helper function to flat a list out of lists

    Parameters
    ----------
    list_of_lists: list

    Returns
    -------
    list
    """
    flat_list = []
    for sublist in list_of_lists:
        for item in sublist:
            flat_list.append(item)
    return flat_list


def path_modules():
    """
    Helper function that prints the modules of the current environment
    """
    import sys
    for file in sys.path:
        print(file)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)