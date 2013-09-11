"""A Python client for Mozilla's basket service."""

# flake8: noqa

from base import (
    BasketException,
    BasketNetworkException,
    confirm,
    confirm_email_change,
    debug_user,
    get_newsletters,
    lookup_user,
    request,
    send_recovery_message,
    send_sms,
    start_email_change,
    subscribe,
    unsubscribe,
    update_user,
    user,
)
