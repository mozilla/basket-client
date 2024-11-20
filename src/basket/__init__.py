"""A Python client for Mozilla's basket service."""

from basket.base import (  # noqa: F401
    BasketException,
    BasketNetworkException,
    confirm,
    get_newsletters,
    lookup_user,
    request,
    send_recovery_message,
    subscribe,
    unsubscribe,
    update_user,
    user,
)

VERSION = "1.2.0"
