"""Unit test to test data deletion."""
from unittest import TestCase

from adefa import cli

from adefa.tests import runner

import mock


class TestCreate(TestCase):
    """Unit test class to test data deletion."""

    def test_delete_project(self):
        cli.client.delete_project = mock.MagicMock()
        result = runner.invoke(cli.delete, ['project', 'arn:aws:devicefarm:us-west-2:xxx'])
        self.assertEqual(result.exit_code, 0)

    def test_delete_upload(self):
        cli.client.delete_upload = mock.MagicMock()
        result = runner.invoke(cli.delete, ['upload', 'arn:aws:devicefarm:us-west-2:xxx'])
        self.assertEqual(result.exit_code, 0)
