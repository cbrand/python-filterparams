# -*- encoding: utf-8 -*-

from filterparams import build_parser

from filterparams_tests.base_parser_test import (
    BaseParserTest
)


class TestSafeParser(BaseParserTest):

    def setUp(self):
        self.filters = []
        self.default_filter = None
        super(TestSafeParser, self).setUp()

    @property
    def parser(self):
        return build_parser(
            self.filters,
            self.default_filter
        )

    @property
    def query(self):
        return self.parser(self.params)

    def test_filter_not_present(self):
        self._add_param('test', filter='eq')
        with self.assertRaises(ValueError):
            self.query

    def test_filter_present(self):
        self.filters.append('eq')
        self._add_param('test', filter='eq')
        self.assertTrue(self.query.has_param('test'))

    def test_default_filter(self):
        self.filters.append('eq')
        self.default_filter = 'eq'
        self._add_param('test')
        param = self.query.get_param('test')
        self.assertEqual(param.filter, 'eq')
