=============
Basket Client
=============

This is a client for Mozilla's email subscription service,
basket_. Basket is not a real subscription service, but it talks to a
real one and we don't really care who/what it is.

There are four API methods: subscribe, unsubscribe, user, and
update_user. View the basket documentation_ for details.

.. image:: https://travis-ci.org/mozilla/basket-client.png
    :target: https://travis-ci.org/mozilla/basket-client
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

Settings
========

BASKET_URL
  | URL to basket server, e.g. ``https://basket.mozilla.org``
  | Default: ``http://localhost:8000``

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
