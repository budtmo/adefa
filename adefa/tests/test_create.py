"""Unit test to test project creation."""
from unittest import TestCase

from adefa import cli

from adefa.tests import runner

import mock


class TestCreate(TestCase):
    """Unit test class to test project creation."""

    @mock.patch('adefa.cli.print_item')
    def test_new_project(self, mocked_print):
        self.assertFalse(mocked_print.called)
        cli.client.create_project = mock.MagicMock(return_value={'project': {'arn': 'value'}})
        result = runner.invoke(cli.create, ['my_project'])
        self.assertTrue(mocked_print.called)
        self.assertEqual(result.exit_code, 0)
