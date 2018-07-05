"""
A set of utility functions that are used in different
parts of the code
"""


def format_types(type_list):
    """ Use to seamlessly format types for rendering in
    the jinja template in scala code.

    It handles nested lists and renders tuples.
    """
    if isinstance(type_list, str):
        return type_list
    elif len(type_list) == 1:
        return "Tuple1[{}]".format(type_list[0])
    return "({})".format(','.join(
        [format_types(i) for i in type_list]))


def quote(word):
    """ Quote a string
    """
    return '\"' + word + '\"'
