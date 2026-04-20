import os

__title__ = 'zelighted'
__version__ = '5.2.0'
__author__ = 'Zebrands'
__author_email__ = 'zetech-checkout@zeb.mx'
__license__ = 'MIT'

from zelighted.http_adapter import HTTPAdapter  # noqa

api_base_url = os.environ.get('ZELIGHTED_API_URL', 'http://localhost:8001/api/v1/')
api_key = os.environ.get('ZELIGHTED_API_KEY') or None
http_adapter = HTTPAdapter()
shared_client = None


def get_shared_client():
    global shared_client
    if not shared_client:
        shared_client = Client()
    return shared_client


def configure(api_key=None, api_base_url=None):
    import zelighted as _z
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    if api_base_url is not None:
        _z.api_base_url = api_base_url

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
