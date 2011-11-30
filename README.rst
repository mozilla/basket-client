Basket-Client
-------------

Basket-Client is a small library for subscribing users to mailing lists through `Basket<https://github.com/mozilla/basket>`.

Usage
=====

    from basket import subscribe

    subscribe('user@example.com', 'basket-email-list-id')

See `the Basket documentation<https://github.com/mozilla/basket/tree/master/apps/news>` for more information.

Settings
========

BASKET_URL
  URL to basket server, e.g. `https://basket.mozilla.com`
