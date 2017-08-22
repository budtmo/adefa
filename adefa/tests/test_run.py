"""Unit test to test scheduling test."""
from unittest import TestCase

from adefa import cli

from adefa.tests import runner

import mock


class TestRun(TestCase):
    """Unit test class to test scheduling test."""

    def test_schedule_test(self):
        cli.client.schedule_run = mock.MagicMock(return_value={'run': {'key1': 'value1'}})
        result = runner.invoke(cli.run, ['-n', 'test_run', '-p', 'test_project', '-a', 'app_id',
                                         '-r', 'APPIUM_PYTHON', '-t', 'test_id', '-g', 'group_id'])
        self.assertEqual(result.exit_code, 0)
