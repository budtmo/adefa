"""Unit test to test print function."""
from unittest import TestCase

from adefa import cli

import mock


class TestPrint(TestCase):
    """Unit test class to test print function."""

    @mock.patch('adefa.cli.print')
    def test_valid_item(self, mocked_print):
        cli.print_item({'key': 'value'})
        mocked_print.assert_called_with('key: value')

    def test_invalid_item(self):
        with self.assertRaises(AttributeError):
            cli.print_item(None)
        with self.assertRaises(AttributeError):
            cli.print_item('mystring')
        with self.assertRaises(AttributeError):
            cli.print_item(1)
        with self.assertRaises(AttributeError):
            cli.print_item(['test'])

    @mock.patch('adefa.cli.print')
    def test_valid_response(self, mocked_print):
        res = [{'key1': 'value1'}, {'key2': 'value2'}]
        cli.print_api_response(res)
        self.assertTrue(mocked_print.called)

    def test_invalid_response(self):
        with self.assertRaises(TypeError):
            cli.print_api_response(None)
        with self.assertRaises(TypeError):
            cli.print_api_response('mystring')
        with self.assertRaises(TypeError):
            cli.print_api_response(1)
        with self.assertRaises(AttributeError):
            cli.print_api_response(['test'])
