.. _install:

========================
Installation & Settings
========================

Install
========

.. code:: bash

    $ pip install basket-client


Settings
========

BASKET_URL
  | URL to basket server, e.g. ``https://basket.mozilla.org``
  | Default: ``http://localhost:8000``

  The URL must not end with ``/``. Basket-client will add ``/`` if needed.

BASKET_API_KEY
  The API Key granted to you by `the mozilla.org developers`_ so that you can
  use the ``lookup_user`` method with an email address.

  .. _the mozilla.org developers: mailto:dev-mozilla-org@lists.mozilla.org

BASKET_TIMEOUT
  | The number of seconds basket client should wait before giving up on the request.
  | Default: ``10``

If you're using Django_ you can simply add these settings to your
``settings.py`` file. Otherwise basket-client will look for these
values in an environment variable of the same name.

.. _Django: https://www.djangoproject.com/


Tests
=====

Tests depend on `hatch` for package management. To install hatch:

.. code:: bash

    $ pip install hatch

Once installed you can run the tests with:

.. code:: bash

    $ hatch run test:all

To run the tests in all supported environments specified via tox:

.. code:: bash

    $ hatch run tox

To run the tests in a specific environment:

.. code:: bash

    $ hatch run tox run -e py310
