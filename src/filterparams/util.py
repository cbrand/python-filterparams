# -*- encoding: utf-8 -*-

import itertools

from werkzeug.datastructures import MultiDict


def to_multidict(value):
    if not isinstance(value, MultiDict) and isinstance(value, dict):
        value = _dict_to_multidict(value)
    return value


def create_key_value_pairs(dictionary, key):
    if hasattr(dictionary, 'getall'):
        get_values = lambda key: dictionary.getall(key)
    else:
        get_values = lambda key: [dictionary.get(key)]

    values = get_values(key)
    return zip([key] * len(values), values)


def _dict_to_multidict(value):
    return MultiDict(
        itertools.chain.from_iterable(
            create_key_value_pairs(value, key)
            for key in value.keys()
        )
    )
