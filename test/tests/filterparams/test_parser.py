# -*- encoding: utf-8 -*-

from unittest import TestCase

from werkzeug.datastructures import MultiDict

from filterparams import parse
from filterparams.obj import (
    And,
    Or,
)


class TestParser(TestCase):
    def setUp(self):
        self.params = {}

    @property
    def query(self):
        return parse(self.params)

    def test_empty_parser(self):
        self.assertEqual(
                len(self.query.params),
                0,
        )

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

    def test_param_parse(self):
        self._add_param(
            'name',
            filter='eq',
            alias='alias',
            value='Doe'
        )
        query = self.query
        param = query.get_param('name')
        self.assertEqual(param.name, 'name')
        self.assertEqual(param.filter, 'eq')
        self.assertEqual(param.alias, 'alias')
        self.assertEqual(param.value, 'Doe')

    def test_single_param_binding_parse(self):
        self._add_param(
            'name',
            filter='eq',
            alias='alias',
            value='Doe'
        )
        query = self.query
        self.assertEqual(query.get_param('name'), query.param_order)

    def test_multiple_param_default_binding(self):
        self._add_param('first_name')
        self._add_param('last_name')
        query = self.query
        self.assertIsInstance(query.param_order, And)

    def test_binding_application(self):
        self._add_param('first_name')
        self._add_param('last_name')
        self._add_binding('first_name|last_name')
        query = self.query
        self.assertIsInstance(query.param_order, Or)

    def _add_order_test(self):
        self.params = MultiDict()
        self._add_param('first_name')
        self._add_param('last_name')
        self.params.add('filter[order]', 'desc(first_name)')
        self.params.add('filter[order]', 'last_name')

    def test_order_application(self):
        self._add_order_test()
        self.assertEqual(len(self.query.orders), 2)

    def test_order_application_first(self):
        self._add_order_test()
        first_order = self.query.orders[0]
        self.assertEqual(first_order.name, 'first_name')

    def test_order_application_orientation_desc(self):
        self._add_order_test()
        first_order = self.query.orders[0]
        self.assertEqual(first_order.direction, 'desc')

    def test_order_application_second(self):
        self._add_order_test()
        second_order = self.query.orders[1]
        self.assertEqual(second_order.name, 'last_name')

    def test_order_application_orentation_asc(self):
        self._add_order_test()
        second_order = self.query.orders[1]
        self.assertEqual(second_order.direction, 'asc')
