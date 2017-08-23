"""Unit test to test get test result."""
from unittest import TestCase

from adefa import cli

from adefa.tests import runner

import mock


class TestResult(TestCase):
    """Unit test class to test get test result."""

    def test_valid_result(self):
        cli.client.get_run = mock.MagicMock(return_value={'run': {'status': 'COMPLETED'}})
        cli.client.list_jobs = mock.MagicMock(return_value={'jobs': [
            {'arn': 'arn:aws:devicefarm:us-west-2:xxx', 'name': 'LG Nexus 5', 'unneded_key1': 'value1'},
            {'arn': 'arn:aws:devicefarm:us-west-2:xxx', 'name': 'Samsung Galaxy S7 Edge', 'unneded_key2': 'value2'}
        ]})
        cli.client.list_artifacts = mock.MagicMock(return_value={'artifacts': [
            {'type': 'result-xml', 'url': 'https://xml', 'unneded_key1': 'value1'},
            {'type': 'video', 'url': 'https://video', 'unneded_key2': 'value2'}
        ]})
        result = runner.invoke(cli.result, ['arn'])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli.result, ['arn', '--json-output'])
        self.assertEqual(result.exit_code, 0)

    def test_pull_attempts(self):
        cli.client.get_run = mock.MagicMock(return_value={'run': {'status': 'IN PROGRESS'}})
        total_attempts = 2
        with mock.patch('time.sleep') as mocked_sleep:
            self.assertFalse(mocked_sleep.called)
            result = runner.invoke(cli.result, ['arn', '-a', total_attempts, '-d', 0.5])
            self.assertTrue(mocked_sleep.called)
            self.assertEqual(total_attempts, mocked_sleep.call_count)
            self.assertEqual(result.exit_code, 0)

    def test_empty_status(self):
        cli.client.get_run = mock.MagicMock(return_value={'run': {'status': None}})
        result = runner.invoke(cli.result, ['arn'])
        self.assertEqual(result.exit_code, 0)

    def test_attribute_error(self):
        cli.client.get_run = mock.MagicMock(return_value=None)
        result = runner.invoke(cli.result, ['arn'])
        self.assertEqual(result.exit_code, -1)

        cli.client.get_run = mock.MagicMock(return_value={'run': {'status': 'COMPLETED'}})
        cli.client.list_jobs = mock.MagicMock(return_value=None)
        result = runner.invoke(cli.result, ['arn'])
        self.assertEqual(result.exit_code, -1)

    def test_key_error(self):
        cli.client.get_run = mock.MagicMock(return_value={
            'run': {'status': 'COMPLETED'}
        })
        cli.client.list_jobs = mock.MagicMock(return_value={'jobs': None})
        result = runner.invoke(cli.result, ['arn'])
        self.assertEqual(result.exit_code, -1)
