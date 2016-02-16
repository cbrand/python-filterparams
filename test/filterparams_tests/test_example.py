# -*- encoding: utf-8 -*-

from unittest import TestCase

from urllib.parse import urlsplit, parse_qs

from filterparams import build_parser
from filterparams.obj import And


class TestExample(TestCase):

    def test_full_run(self):
        url = urlsplit(
            '/users?filter[param][name][like][no_brand_name]=doe'
            '&filter[param][first_name]=doe%&filter[binding]='
            '(!no_brand_name%26first_name)&filter[order]=name'
            '&filter[order]=desc(first_name)'
        )
        params = parse_qs(url.query)

        valid_filters = ['eq', 'like']
        default_filter = 'eq'

        parser = build_parser(
            valid_filters=valid_filters,
            default_filter=default_filter,
        )

        query = parser(params)
        self.assertIsInstance(
            query.param_order,
            And,
        )
        self.assertEqual(
            query.orders[0].name,
            'name',
        )
        self.assertEqual(
            query.orders[1].name,
            'first_name'
        )
