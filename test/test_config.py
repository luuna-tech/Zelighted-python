import os
import unittest
from unittest.mock import patch, MagicMock

import zelighted


class TestEnvironments(unittest.TestCase):

    def test_environments_dict_has_all_presets(self):
        self.assertIn('develop', zelighted.ENVIRONMENTS)
        self.assertIn('staging', zelighted.ENVIRONMENTS)
        self.assertIn('production', zelighted.ENVIRONMENTS)
        self.assertEqual(zelighted.ENVIRONMENTS['develop'], 'http://localhost:8001/api/v1/')
        self.assertEqual(zelighted.ENVIRONMENTS['staging'], 'https://api-stg.zeb.mx/api/v1/')
        self.assertEqual(zelighted.ENVIRONMENTS['production'], 'https://api.zeb.mx/api/v1/')


class TestAutoDetection(unittest.TestCase):

    def setUp(self):
        self._orig_api_key = zelighted.api_key
        self._orig_api_base_url = zelighted.api_base_url

    def tearDown(self):
        zelighted.api_key = self._orig_api_key
        zelighted.api_base_url = self._orig_api_base_url

    def test_zelighted_env_develop(self):
        with patch.dict(os.environ, {'ZELIGHTED_ENV': 'develop'}, clear=False):
            import importlib
            import zelighted as _z
            importlib.reload(_z)
            self.assertEqual(_z.api_base_url, _z.ENVIRONMENTS['develop'])

    def test_zelighted_env_staging(self):
        with patch.dict(os.environ, {'ZELIGHTED_ENV': 'staging'}, clear=False):
            import importlib
            import zelighted as _z
            importlib.reload(_z)
            self.assertEqual(_z.api_base_url, _z.ENVIRONMENTS['staging'])

    def test_zelighted_env_production(self):
        with patch.dict(os.environ, {'ZELIGHTED_ENV': 'production'}, clear=False):
            import importlib
            import zelighted as _z
            importlib.reload(_z)
            self.assertEqual(_z.api_base_url, _z.ENVIRONMENTS['production'])

    def test_zelighted_env_unset_defaults_to_develop(self):
        env = {k: v for k, v in os.environ.items() if k != 'ZELIGHTED_ENV'}
        with patch.dict(os.environ, env, clear=True):
            import importlib
            import zelighted as _z
            importlib.reload(_z)
            self.assertEqual(_z.api_base_url, _z.ENVIRONMENTS['develop'])

    def test_zelighted_env_invalid_defaults_to_develop(self):
        with patch.dict(os.environ, {'ZELIGHTED_ENV': 'foobar'}, clear=False):
            import importlib
            import zelighted as _z
            importlib.reload(_z)
            self.assertEqual(_z.api_base_url, _z.ENVIRONMENTS['develop'])

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


class TestCurrentEnv(unittest.TestCase):

    def setUp(self):
        self._orig_api_base_url = zelighted.api_base_url

    def tearDown(self):
        zelighted.api_base_url = self._orig_api_base_url

    def test_current_env_develop(self):
        zelighted.api_base_url = zelighted.ENVIRONMENTS['develop']
        self.assertEqual(zelighted.current_env(), 'develop')

    def test_current_env_staging(self):
        zelighted.api_base_url = zelighted.ENVIRONMENTS['staging']
        self.assertEqual(zelighted.current_env(), 'staging')

    def test_current_env_production(self):
        zelighted.api_base_url = zelighted.ENVIRONMENTS['production']
        self.assertEqual(zelighted.current_env(), 'production')

    def test_current_env_custom(self):
        zelighted.api_base_url = 'https://custom.example.com/api/'
        self.assertEqual(zelighted.current_env(), 'custom')


class TestConfigure(unittest.TestCase):

    def setUp(self):
        self._orig_api_key = zelighted.api_key
        self._orig_api_base_url = zelighted.api_base_url

    def tearDown(self):
        zelighted.api_key = self._orig_api_key
        zelighted.api_base_url = self._orig_api_base_url

    def test_configure_env(self):
        zelighted.configure(env='staging')
        self.assertEqual(zelighted.api_base_url, zelighted.ENVIRONMENTS['staging'])

    def test_configure_api_key(self):
        zelighted.configure(api_key='newkey')
        self.assertEqual(zelighted.api_key, 'newkey')

    def test_configure_explicit_url_overrides_env(self):
        zelighted.configure(env='production', api_base_url='https://custom.example.com/')
        self.assertEqual(zelighted.api_base_url, 'https://custom.example.com/')

    def test_configure_explicit_url_alone(self):
        zelighted.configure(api_base_url='https://custom.example.com/')
        self.assertEqual(zelighted.api_base_url, 'https://custom.example.com/')

    def test_configure_invalid_env_raises(self):
        with self.assertRaises(ValueError):
            zelighted.configure(env='unknown')

    def test_configure_does_not_change_key_if_not_provided(self):
        zelighted.api_key = 'original'
        zelighted.configure(env='staging')
        self.assertEqual(zelighted.api_key, 'original')

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
            zelighted.configure(env='develop')
        except Exception as e:
            self.fail("configure() raised unexpectedly: %s" % e)
        finally:
            if orig is None:
                del sys.modules['dotenv']
            else:
                sys.modules['dotenv'] = orig


class TestClientEnvParam(unittest.TestCase):

    def setUp(self):
        self._orig_api_key = zelighted.api_key
        self._orig_api_base_url = zelighted.api_base_url
        zelighted.api_key = 'testkey'
        zelighted.api_base_url = zelighted.ENVIRONMENTS['develop']

    def tearDown(self):
        zelighted.api_key = self._orig_api_key
        zelighted.api_base_url = self._orig_api_base_url

    def test_client_env_staging(self):
        client = zelighted.Client(api_key='k', env='staging')
        self.assertEqual(client.api_base_url, zelighted.ENVIRONMENTS['staging'])

    def test_client_env_production(self):
        client = zelighted.Client(api_key='k', env='production')
        self.assertEqual(client.api_base_url, zelighted.ENVIRONMENTS['production'])

    def test_client_explicit_url_overrides_env(self):
        client = zelighted.Client(api_key='k', env='production',
                                  api_base_url='https://custom.example.com/')
        self.assertEqual(client.api_base_url, 'https://custom.example.com/')

    def test_client_invalid_env_raises(self):
        with self.assertRaises(ValueError):
            zelighted.Client(api_key='k', env='badenv')

    def test_client_no_env_uses_module_default(self):
        zelighted.api_base_url = zelighted.ENVIRONMENTS['staging']
        client = zelighted.Client(api_key='k')
        self.assertEqual(client.api_base_url, zelighted.ENVIRONMENTS['staging'])
