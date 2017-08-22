"""Unit test to test print function."""
from unittest import TestCase

from adefa import cli

import mock


class TestPrint(TestCase):
    """Unit test class to test print function."""

    def setUp(self):
        self.items = [None, 'myString', 1]

    @mock.patch('adefa.cli.print')
    def test_valid_item(self, mocked_print):
        cli.print_item({'key': 'value'})
        mocked_print.assert_called_with('key: value')

    def test_invalid_item(self):
        for i in self.items:
            with self.assertRaises(AttributeError):
                cli.print_item(i)

    @mock.patch('adefa.cli.print')
    def test_valid_response(self, mocked_print):
        cli.print_api_response([{'key1': 'value1'}, {'key2': 'value2'}])
        self.assertTrue(mocked_print.called)

    def test_invalid_response(self):
        for i in self.items:
            with self.assertRaises(TypeError):
                cli.print_api_response(i)
