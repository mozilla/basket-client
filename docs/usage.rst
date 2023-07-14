.. _usage:

======================
Usage
======================


Do you want to subscribe people to Mozilla's newsletters?

All you need to do is:

.. code:: python

    import basket

    basket.subscribe("<email>", "<newsletter>", <kwargs>)

You can pass additional fields as keyword arguments, such as format
and country.

Are you checking to see if a user was successfully subscribed? You can
use the ``lookup_user`` method like so:

.. code:: python

    import basket

    basket.lookup_user(email="<email>", api_key="<api_key>")

And it will return full details about the user. <api_key> is a special
token that grants you admin access to the data. Check with `the mozilla.org
developers`_ to get it.

.. _the mozilla.org developers: mailto:dev-mozilla-org@lists.mozilla.org

On most errors, BasketException will be raised. The ``code`` attribute on
the exception object will contain a numeric code indicating the problem,
and the ``desc`` attribute will have a short English description of it.
(Use the ``code`` attribute to determine which error happened, but you
can use ``desc`` in log messages etc.)

Example::

    from basket import errors, some_basket_call

    try:
        rc = some_basket_call(args)
    except BasketError as e:
        if e.code == errors.BASKET_INVALID_EMAIL:
            print("That email address was not valid")
        else:
            log.exception("Some basket error %s", e.desc)

The error codes are defined in ``basket.errors``.  New ones can be added anytime,
but to start with, the errors are::

    BASKET_NETWORK_FAILURE
    BASKET_INVALID_EMAIL
    BASKET_UNKNOWN_EMAIL
    BASKET_UNKNOWN_TOKEN
    BASKET_USAGE_ERROR
    BASKET_EMAIL_PROVIDER_AUTH_FAILURE
    BASKET_AUTH_ERROR
    BASKET_SSL_REQUIRED
    BASKET_INVALID_NEWSLETTER
    BASKET_INVALID_LANGUAGE
    BASKET_EMAIL_NOT_CHANGED
    BASKET_CHANGE_REQUEST_NOT_FOUND

    # If you get this, report it as a bug so we can add a more specific
    # error code.
    BASKET_UNKNOWN_ERROR

Usage in tests
==============

You may wish to test your site without the overhead and fragility of calling
an external service. To test your subscription forms without actually hitting
the Basket service simply use a special set of email addresses:

* ``success@example.com`` will cause the basket client to return a success message.
* ``failure@example.com`` will cause the basket client to raise a ``BasketError`` exception.

These will allow you to test the functioning of your form handling code without making any
actual network calls.
