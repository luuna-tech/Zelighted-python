import os

__title__ = 'zelighted'
__version__ = '5.1.0'
__author__ = 'Zebrands'
__license__ = 'MIT'

from zelighted.http_adapter import HTTPAdapter  # noqa

ENVIRONMENTS = {
    'develop': 'http://localhost:8001/api/v1/',
    'staging': 'https://api-stg.zeb.mx/api/v1/',
    'production': 'https://api.zeb.mx/api/v1/',
}

_env = os.environ.get('ZELIGHTED_ENV', 'develop')
if _env not in ENVIRONMENTS:
    _env = 'develop'

api_key = os.environ.get('ZELIGHTED_API_KEY') or None
api_base_url = ENVIRONMENTS[_env]
http_adapter = HTTPAdapter()
shared_client = None


def get_shared_client():
    global shared_client
    if not shared_client:
        shared_client = Client()
    return shared_client


def current_env():
    import zelighted as _z
    for name, url in ENVIRONMENTS.items():
        if url == _z.api_base_url:
            return name
    return 'custom'


def configure(env=None, api_key=None, api_base_url=None):
    import zelighted as _z
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    if api_base_url is not None:
        _z.api_base_url = api_base_url
    elif env is not None:
        if env not in ENVIRONMENTS:
            raise ValueError("env must be one of: %s" % ', '.join(ENVIRONMENTS))
        _z.api_base_url = ENVIRONMENTS[env]

    if api_key is not None:
        _z.api_key = api_key


from zelighted.client import Client  # noqa
from zelighted.resource import (  # noqa
    Metrics,
    Person,
    SurveyRequest,
    SurveyResponse,
    Unsubscribe,
    Bounce,
    AutopilotConfiguration,
    AutopilotMembership,
    AutopilotMembershipForEmail,
    AutopilotMembershipForSms,
)
