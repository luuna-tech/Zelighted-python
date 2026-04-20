class ZelightedError(Exception):

    def __init__(self, response):
        self.response = response

    def __repr__(self):
        return "<%d: %s>" % (self.response.status_code, self.response.body)

    __str__ = __repr__


class AuthenticationError(ZelightedError):
    """401, api auth missing or incorrect."""
    pass


class UnsupportedFormatRequestedError(ZelightedError):
    """406, invalid format in Accept header."""
    pass


class ResourceValidationError(ZelightedError):
    """422, validation errors."""
    pass


class TooManyRequestsError(ZelightedError):
    """429, rate limited."""

    def __init__(self, response):
        super(TooManyRequestsError, self).__init__(response)
        self.retry_after = int(response.headers['Retry-After'])


class GeneralAPIError(ZelightedError):
    """500, general/unknown error."""
    pass


class ServiceUnavailableError(ZelightedError):
    """503, maintenance or overloaded."""
    pass
