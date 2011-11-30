Basket-Client
-------------

Basket-Client is a small library for subscribing users to mailing lists through basket_.

.. _basket: https://github.com/mozilla/basket

Usage
=====

    from basket import subscribe

    subscribe('user@example.com', 'basket-email-list-id')

See the basket documentation_ for more information and a list of
available newsletters.

.. _documentation: https://github.com/mozilla/basket/tree/master/apps/news

Settings
========

BASKET_URL
  URL to basket server, e.g. `https://basket.mozilla.com`
