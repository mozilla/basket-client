=============
Basket Client
=============

This is a client for Mozilla's email subscription service,
basket_. Basket is not a real subscription service, but it talks to a
real one and we don't really care who/what it is.

There are multiple API methods. View the basket documentation_ for details.

.. image:: https://travis-ci.org/mozilla/basket-client.png
    :target: https://travis-ci.org/mozilla/basket-client
.. image:: https://coveralls.io/repos/mozilla/basket-client/badge.png?branch=master
    :target: https://coveralls.io/r/mozilla/basket-client
.. image:: https://pypip.in/v/basket-client/badge.png
    :target: https://crate.io/packages/basket-client

.. _basket: https://github.com/mozilla/basket

Installation
============

.. code:: bash

    $ pip install basket-client

Usage
=====

Do you want to subscribe people to Mozilla's newsletters?
All you need to do is:

.. code:: python

    import basket

    basket.subscribe('<email>', '<newsletter>', <kwargs>)

You can pass additional fields as keyword arguments, such as format
and country. For a list of available fields and newsletters, see the
basket documentation_.

.. _documentation: https://github.com/mozilla/basket/#readme

Are you checking to see if a user was successfully subscribed? You can
use the ``lookup_user`` method like so:

.. code:: python

    import basket

    basket.lookup_user(email='<email>', api_key='<api_key>')

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
            print "That email address was not valid"
        else:
            log.exception("Some basket error (%s)" % e.desc)

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


Settings
========

BASKET_URL
  | URL to basket server, e.g. ``https://basket.mozilla.org``
  | Default: ``http://localhost:8000``

  The URL must not end with ``/``. Basket-client will add ``/`` if needed.

BASKET_API_KEY
  The API Key granted to you by `the mozilla.org developers`_ so that you can
  use the ``lookup_user`` method with an email address.

BASKET_TIMEOUT
  | The number of seconds basket client should wait before giving up on the request.
  | Default: ``10``

If you're using Django_ you can simply add these settings to your
``settings.py`` file. Otherwise basket-client will look for these
values in an environment variable of the same name.

.. _Django: https://www.djangoproject.com/

Tests
=====

To run tests:

.. code:: bash

    $ python setup.py test

Change Log
==========

v0.3.9
------

* Add numeric error codes.

v0.3.8
------

* Add the ``start_email_change`` and ``confirm_email_change`` functions.

v0.3.7
------

* Add the ``lookup_user`` function.
* Add the ``BASKET_API_KEY`` setting.
* Add the ``BASKET_TIMEOUT`` setting.

v0.3.6
------

* Add the ``confirm`` function.

v0.3.5
------

* Add tests

v0.3.4
------

* Fix issue with calling ``subscribe`` with an iterable of newsletters.
* Add ``request`` function to those exposed by the ``basket``` module.

v0.3.3
------

* Add get_newsletters API method for information on currently available newsletters.
* Handle Timeout exceptions from requests.
