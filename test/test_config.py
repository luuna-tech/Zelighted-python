import os
import unittest
from unittest.mock import patch, MagicMock

import zelighted


class TestApiBaseUrl(unittest.TestCase):

    def setUp(self):
        self._orig_api_base_url = zelighted.api_base_url

    def tearDown(self):
        zelighted.api_base_url = self._orig_api_base_url

    def test_default_url_is_localhost(self):
        env = {k: v for k, v in os.environ.items() if k != 'ZELIGHTED_API_URL'}
        with patch.dict(os.environ, env, clear=True):
            import importlib
            import zelighted as _z
            importlib.reload(_z)
            self.assertEqual(_z.api_base_url, 'http://localhost:8001/api/v1/')

    def test_zelighted_api_url_env_var_overrides_default(self):
        with patch.dict(os.environ, {'ZELIGHTED_API_URL': 'https://api.zeb.mx/api/v1/'}, clear=False):
            import importlib
            import zelighted as _z
            importlib.reload(_z)
            self.assertEqual(_z.api_base_url, 'https://api.zeb.mx/api/v1/')

    def test_zelighted_api_url_staging(self):
        with patch.dict(os.environ, {'ZELIGHTED_API_URL': 'https://api-stg.zeb.mx/api/v1/'}, clear=False):
            import importlib
            import zelighted as _z
            importlib.reload(_z)
            self.assertEqual(_z.api_base_url, 'https://api-stg.zeb.mx/api/v1/')

    def test_zelighted_api_key_auto_detection(self):
        with patch.dict(os.environ, {'ZELIGHTED_API_KEY': 'mykey123'}, clear=False):
            import importlib
            import zelighted as _z
            importlib.reload(_z)
            self.assertEqual(_z.api_key, 'mykey123')

    def test_zelighted_api_key_unset_is_none(self):
        env = {k: v for k, v in os.environ.items() if k != 'ZELIGHTED_API_KEY'}
        with patch.dict(os.environ, env, clear=True):
            import importlib
            import zelighted as _z
            importlib.reload(_z)
            self.assertIsNone(_z.api_key)


class TestConfigure(unittest.TestCase):

    def setUp(self):
        self._orig_api_key = zelighted.api_key
        self._orig_api_base_url = zelighted.api_base_url

    def tearDown(self):
        zelighted.api_key = self._orig_api_key
        zelighted.api_base_url = self._orig_api_base_url

    def test_configure_api_key(self):
        zelighted.configure(api_key='newkey')
        self.assertEqual(zelighted.api_key, 'newkey')

    def test_configure_explicit_url(self):
        zelighted.configure(api_base_url='https://custom.example.com/')
        self.assertEqual(zelighted.api_base_url, 'https://custom.example.com/')

    def test_configure_both_api_key_and_url(self):
        zelighted.configure(api_base_url='https://api.zeb.mx/api/v1/', api_key='mykey')
        self.assertEqual(zelighted.api_base_url, 'https://api.zeb.mx/api/v1/')
        self.assertEqual(zelighted.api_key, 'mykey')

    def test_configure_does_not_change_key_if_not_provided(self):
        zelighted.api_key = 'original'
        zelighted.configure(api_base_url='https://custom.example.com/')
        self.assertEqual(zelighted.api_key, 'original')

    def test_configure_does_not_change_url_if_not_provided(self):
        zelighted.api_base_url = 'https://custom.example.com/'
        zelighted.configure(api_key='newkey')
        self.assertEqual(zelighted.api_base_url, 'https://custom.example.com/')

    def test_configure_loads_dotenv_if_available(self):
        mock_load = MagicMock()
        with patch.dict('sys.modules', {'dotenv': MagicMock(load_dotenv=mock_load)}):
            zelighted.configure()
        mock_load.assert_called_once()

    def test_configure_silently_skips_dotenv_if_not_installed(self):
        import sys
        orig = sys.modules.get('dotenv')
        sys.modules['dotenv'] = None
        try:
            zelighted.configure(api_base_url='http://localhost:8001/api/v1/')
        except Exception as e:
            self.fail("configure() raised unexpectedly: %s" % e)
        finally:
            if orig is None:
                del sys.modules['dotenv']
            else:
                sys.modules['dotenv'] = orig


class TestClientUrlParam(unittest.TestCase):

    def setUp(self):
        self._orig_api_key = zelighted.api_key
        self._orig_api_base_url = zelighted.api_base_url
        zelighted.api_key = 'testkey'
        zelighted.api_base_url = 'http://localhost:8001/api/v1/'

    def tearDown(self):
        zelighted.api_key = self._orig_api_key
        zelighted.api_base_url = self._orig_api_base_url

    def test_client_explicit_url(self):
        client = zelighted.Client(api_key='k', api_base_url='https://api.zeb.mx/api/v1/')
        self.assertEqual(client.api_base_url, 'https://api.zeb.mx/api/v1/')

    def test_client_no_url_uses_module_default(self):
        zelighted.api_base_url = 'https://api-stg.zeb.mx/api/v1/'
        client = zelighted.Client(api_key='k')
        self.assertEqual(client.api_base_url, 'https://api-stg.zeb.mx/api/v1/')

    def test_client_programmatic_override(self):
        client = zelighted.Client(api_key='k', api_base_url='https://custom.example.com/')
        self.assertEqual(client.api_base_url, 'https://custom.example.com/')
