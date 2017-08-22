"""Unit test to test get list of data."""
from unittest import TestCase

from adefa import cli

from adefa.tests import runner

import mock


@mock.patch('adefa.cli.print_api_response')
class TestList(TestCase):
    """Unit test class to test get list of data."""

    def test_list(self, mocked_print):
        items = ['devices', 'projects', 'groups', 'uploads', 'runs']
        for pos, item in enumerate(items):
            cli.client = mock.MagicMock()
            if pos > 1:
                with mock.patch('click.prompt') as mocked_click:
                    result = runner.invoke(cli.list, [item])
                    self.assertTrue(mocked_click.called)
            else:
                result = runner.invoke(cli.list, [item])
            self.assertTrue(mocked_print.called)
            self.assertEqual(result.exit_code, 0)
