"""Unit test to test project creation."""
from unittest import TestCase

from adefa import cli

from adefa.tests import runner

import mock


class TestCreate(TestCase):
    """Unit test class to test project creation."""

    def test_create_project(self):
        cli.client.create_project = mock.MagicMock(return_value={'project': {'arn': 'value'}})
        result = runner.invoke(cli.create, ['my_project'])
        self.assertEqual(result.exit_code, 0)
