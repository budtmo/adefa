"""Unit test to test get list of data."""
from unittest import TestCase

from adefa import cli

from adefa.tests import runner

import mock


class TestList(TestCase):
    """Unit test class to test get list of data."""

    @mock.patch('adefa.cli.print_api_response')
    def test_projects(self, mocked_print):
        self.assertFalse(mocked_print.called)
        cli.client.list_projects = mock.MagicMock(return_value={'projects': [{'key1': 'key2'}]})
        result = runner.invoke(cli.list, ['projects'])
        self.assertTrue(mocked_print.called)
        self.assertEqual(result.exit_code, 0)
