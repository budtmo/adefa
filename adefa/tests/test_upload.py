"""Unit test to test uploading data."""
from unittest import TestCase

from adefa import cli

from adefa.tests import runner

import mock

import requests


class TestUpload(TestCase):
    """Unit test class to test uploading data."""

    def test_local_path(self):
        with mock.patch('builtins.open', mock.mock_open()):
            cli.client.create_upload = mock.MagicMock(return_value={'upload': {'url': 'https://test', 'arn': 'arn'}})
            requests.put = mock.MagicMock()
            result = runner.invoke(cli.upload, ['-n', 'test_upload', '-p', 'test_project', '-f', 'app.apk',
                                                '-t', 'ANDROID_APP'])
            self.assertEqual(result.exit_code, 0)

    def test_url_path(self):
        with mock.patch('urllib.request.urlopen'):
            cli.client.create_upload = mock.MagicMock(return_value={'upload': {'url': 'https://test', 'arn': 'arn'}})
            requests.put = mock.MagicMock()
            result = runner.invoke(cli.upload, ['-n', 'test_upload', '-p', 'test_project', '-f', 'https://app.apk',
                                                '-t', 'ANDROID_APP'])
            self.assertEqual(result.exit_code, 0)

    def test_invalid_type(self):
        result = runner.invoke(cli.upload, ['-n', 'test_upload', '-p', 'test_project', '-f', 'app.apk',
                                            '-t', 'invalidtype'])
        self.assertEqual(result.exit_code, 2)
