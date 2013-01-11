"""A Python client for Mozilla's basket service."""

from base import (send_sms, subscribe, unsubscribe, user,
                  update_user, debug_user, BasketException)


VERSION = (0, 3, 1)

__version__ = '.'.join(map(str, VERSION))
__author__ = 'Michael Kelly and contributors'
__contact__ = 'dev-mozilla-org@lists.mozilla.org'
__homepage__ = 'https://github.com/mozilla/basket-client'
__license__ = 'BSD'
