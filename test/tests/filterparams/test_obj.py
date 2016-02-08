# -*- encoding: utf-8 -*-

from unittest import TestCase

from filterparams.obj import (
    Parameter,
    And,
    Or,
    Not,
)


class TestObj(TestCase):

    def test_eq_param(self):
        self.assertEqual(
            Parameter("q1"),
            Parameter("q1"),
        )

    def test_neq_param(self):
        self.assertNotEqual(
            Parameter("q1"),
            Parameter("q2"),
        )

    def test_neq_param_other(self):
        self.assertNotEqual(
            Parameter("q1"),
            And("a", "b"),
        )

    def test_and_eq(self):
        self.assertEqual(
            And("q1", "q2"),
            And("q1", "q2"),
        )

    def test_and_neq(self):
        self.assertNotEqual(
            And("q1", "q2"),
            And("q1", "q3"),
        )

    def test_and_neq_other_type(self):
        self.assertNotEqual(
            And("q1", "q2"),
            Or("q1", "q2"),
        )

    def test_or_eq(self):
        self.assertEqual(
            Or("q1", "q2"),
            Or("q1", "q2"),
        )

    def test_or_neq(self):
        self.assertNotEqual(
            Or("q1", "q2"),
            Or("q1", "q1"),
        )

    def test_or_neq_other_type(self):
        self.assertNotEqual(
            Or("q1", "q2"),
            And("q1", "q2"),
        )

    def test_not_eq(self):
        self.assertEqual(
            Not("q1"),
            Not("q1"),
        )

    def test_not_neq(self):
        self.assertNotEqual(
            Not("q1"),
            Not("q2"),
        )

    def test_not_neq_other_type(self):
        self.assertNotEqual(
            Not("q1"),
            "q1"
        )
