import json
import logging
import os

# Use Django settings for BASKET_URL if available, but fall back to
# env var or default if not. This lets us test without all the setup
# that we'd otherwise need for Django.
try:
    from django.conf import settings
except (ImportError, AttributeError):
    # Django not installed
    settings = None
else:
    if not settings.configured:
        # Django installed but not initialized
        settings = None

import requests

import basket.errors as errors


log = logging.getLogger(__name__)


def get_env_or_setting(name, default=None):
    """Return the value of name from an env var, a Django setting, or default"""
    return os.getenv(name, getattr(settings, name, default))


BASKET_URL = get_env_or_setting('BASKET_URL', 'http://localhost:8000')
BASKET_API_KEY = get_env_or_setting('BASKET_API_KEY', '')
BASKET_TIMEOUT = get_env_or_setting('BASKET_TIMEOUT', 10)


class BasketException(Exception):
    def __init__(self, *args, **kwargs):
        # Required kwargs:
        #
        # :param code: Basket error code (from basket/errors.py)
        #
        # Optional args:
        #
        # :param: First arg can be an English description of the error
        #
        # Optional kwargs:
        #
        # :param status_code: HTTP status code (e.g. 200, 400)
        # :param result: Whole decoded result from Basket
        #
        self.status_code = kwargs.pop('status_code', 0)
        # `code` is a required kwarg, but if it's not there, better to
        # fake it and report the error than to blow up in the middle of error
        # handling.
        self.code = kwargs.pop('code', errors.BASKET_UNKNOWN_ERROR)
        self.result = kwargs.pop('result', {})
        if args:
            self.desc = args[0]
        else:
            self.desc = ''
        super(BasketException, self).__init__(*args, **kwargs)


class BasketNetworkException(BasketException):
    """Used on error connecting to basket"""
    def __init__(self, *args, **kwargs):
        if 'code' not in kwargs:
            kwargs['code'] = errors.BASKET_NETWORK_FAILURE
        super(BasketNetworkException, self).__init__(*args, **kwargs)


def basket_url(method, token=None):
    """Form a basket API url. If the request requires a user-specific
    token, it is suffixed as the last part of the URL."""

    token = '%s/' % token if token else ''

    return ('%s/news/%s/%s' % (BASKET_URL, method, token))


def parse_response(res):
    """Parse the result of a basket API call, raise exception on error"""

    # Parse the json and check for errors
    # We assume all basket calls respond with JSON (they're supposed to)
    result = {}
    try:
        result = json.loads(res.content)
    except:
        log.exception("Error parsing JSON returned by basket (%s)" % res.content)

    if res.status_code != 200 or result.get('status', '') == 'error':
        desc = result.get('desc', '%s request returned from basket: %s' %
                                  (res.status_code, res.content))
        raise BasketException(desc,
                              status_code=res.status_code,
                              code=result.get('code', errors.BASKET_UNKNOWN_ERROR),
                              result=result)

    return result


def request(method, action, data=None, token=None, params=None, headers=None):
    """Call the basket API with the supplied http method and data."""

    # newsletters should be comma-delimited
    if data and 'newsletters' in data:
        if not isinstance(data['newsletters'], basestring):
            data['newsletters'] = ','.join(data['newsletters'])

    try:
        res = requests.request(method,
                               basket_url(action, token),
                               data=data,
                               params=params,
                               headers=headers,
                               timeout=BASKET_TIMEOUT)
    except requests.exceptions.ConnectionError:
        raise BasketNetworkException("Error connecting to basket")
    except requests.exceptions.Timeout:
        raise BasketNetworkException("Timeout connecting to basket")
    return parse_response(res)


# Public API methods

def confirm(token):
    """
    Confirm a user.  token is required.
    """
    return request('post', 'confirm', token=token)


def subscribe(email, newsletters, **kwargs):
    """Subscribe an email through basket to `newsletters`, which can
    be string or an array of newsletter names. Additional parameters
    should be passed as keyword arguments."""

    kwargs.update(email=email, newsletters=newsletters)
    headers = {}
    if kwargs.get('sync', 'N') == 'Y':
        api_key = kwargs.pop('api_key', BASKET_API_KEY)
        if not api_key:
            raise BasketException('API key required for email lookup.',
                                  code=errors.BASKET_AUTH_ERROR)
        headers['x-api-key'] = api_key

    source_ip = kwargs.pop('source_ip', None)
    if source_ip:
        headers['x-source-ip'] = source_ip

    return request('post', 'subscribe', data=kwargs, headers=headers)


def send_sms(mobile_number, msg_name, optin=False, source_ip=None):
    """
    Send SMS message `msg_name` to `mobile_number` and optionally add the
    number to a list for future messages.
    """
    headers = {}
    if source_ip:
        headers['x-source-ip'] = source_ip

    return request('post', 'subscribe_sms', data={
        'mobile_number': mobile_number,
        'msg_name': msg_name,
        'optin': 'Y' if optin else 'N',
    }, headers=headers)


def unsubscribe(token, email, newsletters=None, optout=False):
    """Unsubscribe an email from certain newsletters, or all of them
    if `optout` is passed. Requires a token."""

    data = {'email': email}

    if optout:
        data['optout'] = 'Y'
    elif newsletters:
        data['newsletters'] = newsletters
    else:
        raise BasketException('unsubscribe requires either a newsletters '
                              'or optout parameter',
                              code=errors.BASKET_USAGE_ERROR)

    return request('post', 'unsubscribe', data=data, token=token)


def user(token):
    """Get all the information about a user. Requires a token."""
    return request('get', 'user', token=token)


def update_user(token, **kwargs):
    """Update any fields for a user. Requires a token. If newsletters
    is passed, the user is only subscribed to those specific
    newsletters."""

    return request('post', 'user', data=kwargs, token=token)


def lookup_user(email=None, token=None, api_key=None):
    """Get a user's information using an API key or the user's token."""
    # prefer token
    if token:
        return request('get', 'lookup-user', params={'token': token})

    if email:
        api_key = api_key or BASKET_API_KEY
        if not api_key:
            raise BasketException('API key required for email lookup.',
                                  code=errors.BASKET_AUTH_ERROR)
        return request('get', 'lookup-user',
                       params={'email': email},
                       headers={'x-api-key': api_key})

    raise BasketException('Either token or email are required.',
                          code=errors.BASKET_USAGE_ERROR)


def debug_user(email, supertoken):
    """Get a user's information using a supertoken only known by devs,
    useful for ensuring that data is being posted correctly"""

    return request('get', 'debug-user',
                   params={'email': email,
                           'supertoken': supertoken})


def send_recovery_message(email):
    """Send recovery message for this email"""
    return request('post', 'recover', data={'email': email})


def get_newsletters():
    """Returns data about the newsletters that basket knows about.
    Format is a list of dictionaries.
    """
    return request('get', 'newsletters')['newsletters']


def start_email_change(token, new_email):
    """
    Start the process of changing the email address for a user.

    :param token: User's subscriber token
    :param new_email: Desired new email address
    """
    return request('post', 'start-email-change', data={'email': new_email}, token=token)


def confirm_email_change(change_key):
    """
    Confirm email change.

    Call this when a user hits the link they were given to confirm changing
    their email. The link includes the change_key in it.
    """
    return request('post', 'confirm-email-change', token=change_key)
