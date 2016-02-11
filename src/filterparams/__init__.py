# -*- encoding: utf-8 -*-

from functools import partial

from .parser import Parser
from .safe_parser import SafeParser


def parse(dictionary):
    return Parser(dictionary).query


def build_parser(valid_filters, default_filter):
    return lambda dictionary: SafeParser(
        dictionary,
        valid_filters=valid_filters,
        default_filter=default_filter,
    ).query
