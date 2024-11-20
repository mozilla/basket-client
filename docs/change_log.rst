.. _change-log:

======================
Change Log
======================

v1.2.0 - Nov 20, 2024
---------------------

* Add support for Python 3.12 and 3.13
* Drop support for Python 3.8
* Remove outdated APIs no longer in Basket
* Add new Basket APIs built on django-ninja -- ``/api/v1/news/newsletters/`` and ``/api/v1/users/lookup/``

v1.1.0 - Jun 14, 2023
---------------------

* Drop support for Python 2.x and < 3.8 (current supported Python versions).

v1.0.0 - Jan 7, 2019
--------------------

* Add support for Python 3.5+ and drop support for Python 2.6.
  Thanks to `diox <https://github.com/diox>`_ for the patch!

v0.3.11
-------

* Add option to send the source IP to basket service for rate limiting purposes for the subscribe and send_sms functions.


v0.3.10
-------

* Set api key on subscribe call when sync=Y

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

