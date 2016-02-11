# -*- encoding: utf-8 -*-

from .parser import Parser


class SafeParser(Parser):
    """
    Usual parser which also verifies the
    supported operations.
    """

    def __init__(self, query_dict, valid_filters, **kwargs):
        super().__init__(query_dict, **kwargs)
        self.filters = valid_filters

    @property
    def _params(self):
        for param in super()._params:
            self._verify_filter_of(param)
            yield param

    def _verify_filter_of(self, parameter):
        if parameter.filter not in self.filters:
            raise ValueError(
                (
                    'The filter {filter} of '
                    'parameter {name} with alias'
                    '{alias} is unknown'
                ).format(
                    name=parameter.name,
                    alias=parameter.alias,
                    filter=parameter.filter,
                )
            )
