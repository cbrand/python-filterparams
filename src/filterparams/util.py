# -*- encoding: utf-8 -*-

import itertools

from werkzeug.datastructures import MultiDict


def to_multidict(value):
    if not isinstance(value, MultiDict) and isinstance(value, dict):
        value = _dict_to_multidict(value)
    return value


def flatten(to_flatten_list):
    if not isinstance(to_flatten_list, (list, tuple)):
        return to_flatten_list

    result = []
    for list_item in to_flatten_list:
        if isinstance(list_item, (list, tuple)):
            result.extend(flatten(item) for item in list_item)
        else:
            result.append(list_item)
    return result


def create_key_value_pairs(dictionary, key):
    if hasattr(dictionary, 'getall'):
        get_values = lambda key: dictionary.getall(key)
    else:
        get_values = lambda key: flatten([dictionary.get(key)])

    values = get_values(key)
    return zip([key] * len(values), values)


def _dict_to_multidict(value):
    return MultiDict(
        itertools.chain.from_iterable(
            create_key_value_pairs(value, key)
            for key in value.keys()
        )
    )
