"""Unit test to test creating device group / pool."""
from unittest import TestCase

from adefa import cli

from adefa.tests import runner

import mock


class TestGroup(TestCase):
    """Unit test class to test creating device group / pool."""

    def test_multiple_devices(self):
        cli.client.create_device_pool = mock.MagicMock(return_value={'devicePool': {'arn': 'arn'}})
        result = runner.invoke(cli.group, ['-n', 'test_group', '-p', 'test_project', '-d', 'device1',
                                           '-d', 'device2'])
        self.assertEqual(result.exit_code, 0)
