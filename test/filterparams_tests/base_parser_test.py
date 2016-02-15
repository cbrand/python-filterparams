# -*- encoding: utf-8 -*-

from unittest import TestCase


class BaseParserTest(TestCase):
    def setUp(self):
        self.params = {}

    def _add_param(self, name, **kwargs):
        items = [name]
        if 'filter' in kwargs:
            items.append(kwargs['filter'])
            if 'alias' in kwargs:
                items.append(kwargs['alias'])
        key = 'filter[param]%s' % (
            ''.join('[%s]' % item for item in items)
        )
        self.params[key] = kwargs.get('value', None)

    def _add_binding(self, binding):
        self.params['filter[binding]'] = binding
