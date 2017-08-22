"""Unit test to test data deletion."""
from unittest import TestCase

from adefa import cli

from adefa.tests import runner

import mock


class TestDelete(TestCase):
    """Unit test class to test data deletion."""

    def test_delete(self):
        cli.client = mock.MagicMock()

        arguments = ['project', 'upload', 'group', 'run']
        for a in arguments:
            delete_operation = runner.invoke(cli.delete, [a, 'arn:aws:devicefarm:us-west-2:xxx'])
            self.assertEqual(delete_operation.exit_code, 0)
