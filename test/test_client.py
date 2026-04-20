import unittest

import zelighted


class ClientTest(unittest.TestCase):

    def test_instantiating_client_requires_api_key(self):
        original_api_key = zelighted.api_key
        try:
            zelighted.api_key = None
            self.assertRaises(ValueError, lambda: zelighted.Client())
            zelighted.Client(api_key='abc123')
        except:
            zelighted.api_key = original_api_key
