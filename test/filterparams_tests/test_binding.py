# -*- encoding: utf-8 -*-

from unittest import TestCase

from funcparserlib.lexer import LexerError
from funcparserlib.parser import NoParseError

from filterparams.binding import loads
from filterparams.obj import (
    Query,
    Parameter,
    Not,
    Or,
    And,
)


class TestBinding(TestCase):
    def setUp(self):
        self.params = ''
        self.query = Query()

    def add_param(self, name):
        self.query.add(
            name=name,
        )

    @property
    def parsed_result(self):
        param, _ = loads(self.params, self.query)
        return param

    def test_param(self):
        self.params = "q1"
        self.add_param("q1")
        self.assertIsInstance(self.parsed_result, Parameter)
        self.assertEqual(self.parsed_result.name, "q1")

    def test_unkown_param(self):
        self.params = "q2"
        self.add_param("q1")
        with self.assertRaises(KeyError):
            self.parsed_result

    def test_unparsable(self):
        self.add_param("q2")
        self.params = "q2|"
        with self.assertRaises(NoParseError):
            self.parsed_result

    def test_unlexable(self):
        self.params = "ä1§"
        with self.assertRaises(LexerError):
            self.parsed_result

    def test_not(self):
        self.params = "!q1"
        self.add_param("q1")

        result = self.parsed_result
        self.assertIsInstance(result, Not)
        param = result.inner
        self.assertEqual(param.name, 'q1')

    def test_or(self):
        self.params = "q1|q2"
        self.add_param("q1")
        self.add_param("q2")

        result = self.parsed_result
        self.assertIsInstance(result, Or)
        self.assertEqual(result.left.name, "q1")
        self.assertEqual(result.right.name, "q2")

    def test_and(self):
        self.params = "q1 & q2"
        self.add_param("q1")
        self.add_param("q2")

        self.assertEqual(self.parsed_result, And(
            "q1", "q2"
        ))

    def test_complex(self):
        for i in range(1, 6):
            self.add_param("q%s" % i)
        self.params = "q1 & q2 | q3 | q4 & !q5"

        self.assertEqual(
            self.parsed_result,
            Or(
                And("q1", "q2"),
                Or(
                    "q3",
                    And(
                        "q4",
                        Not("q5"),
                    )
                )
            )
        )

    def test_brackets(self):
        for i in range(1, 7):
            self.add_param("q%s" % i)
        self.params = "q1 & ((q2 |q3| q4) & !(q5 & q6))"
        self.assertEqual(
            self.parsed_result,
            And(
                "q1",
                And(
                    Or("q2", Or("q3", "q4")),
                    Not(And("q5", "q6"))
                )
            )
        )
