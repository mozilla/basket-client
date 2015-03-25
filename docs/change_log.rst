.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _change-log:

======================
Change Log
======================

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

