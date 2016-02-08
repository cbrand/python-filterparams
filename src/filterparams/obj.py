# -*- encoding: utf-8 -*-

from collections import namedtuple


class Query:
    def __init__(self):
        self._parameters = {}
        self.orders = []

    def add(self, name, **kwargs):
        return self.add_param(
                Parameter(
                        name=name,
                        **kwargs
                )
        )

    def add_param(self, parameter):
        self._parameters[parameter.name] = parameter

    def get_param(self, name):
        return self._parameters[name]


class Parameter:
    def __init__(self, name, **kwargs):
        self.name = name
        self.filter = kwargs.get('filter', None)
        self.value = kwargs.get('value', None)

    def __eq__(self, other):
        other = getattr(other, 'name', other)
        return other == self.name


class BindingOperation:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return (
            self.left == other.left and
            self.right == other.right
        )


class And(BindingOperation):
    def __eq__(self, other):
        if not isinstance(other, And):
            return False
        return super().__eq__(other)


class Or(BindingOperation):
    def __eq__(self, other):
        if not isinstance(other, Or):
            return False
        return super().__eq__(other)


class Not:
    def __init__(self, inner):
        self.inner = inner

    def __eq__(self, other):
        if not isinstance(other, Not):
            return False
        return self.inner == other.inner
