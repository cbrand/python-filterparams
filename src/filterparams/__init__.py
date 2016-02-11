# -*- encoding: utf-8 -*-

from .parser import Parser


def parse(dictionary):
    return Parser(dictionary).query
