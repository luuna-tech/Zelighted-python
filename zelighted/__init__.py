__title__ = 'zelighted'
__version__ = '5.0.0'
__author__ = 'Zebrands'
__license__ = 'MIT'

from zelighted.http_adapter import HTTPAdapter  # noqa

api_key = None
api_base_url = 'http://localhost:8001/api/v1/'
http_adapter = HTTPAdapter()
shared_client = None


def get_shared_client():
    global shared_client
    if not shared_client:
        shared_client = Client()
    return shared_client


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
