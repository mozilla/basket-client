import json
import unittest
from unittest.mock import ANY, Mock, patch

from requests.exceptions import ConnectionError, Timeout

from basket import (
    BasketException,
    confirm,
    errors,
    get_newsletters,
    lookup_user,
    request,
    send_recovery_message,
    subscribe,
    unsubscribe,
    update_user,
    user,
)
from basket.base import basket_url, get_env_or_setting, parse_response

# Warning: there are two request() methods, one in basket-client and
# one in the requests library. Pay attention, it's very confusing.


class TestBasketClient(unittest.TestCase):
    def test_basket_url_no_token(self):
        """Form basket URL properly when no token used"""
        with patch("basket.base.BASKET_URL", new="BASKET_URL"):
            result = basket_url("METHOD")
        self.assertEqual("BASKET_URL/news/METHOD/", result)

    def test_basket_url_with_token(self):
        """Form basket URL properly when token used"""
        with patch("basket.base.BASKET_URL", new="BASKET_URL"):
            result = basket_url("METHOD", "TOKEN")
        self.assertEqual("BASKET_URL/news/METHOD/TOKEN/", result)

    def test_response_not_200(self):
        """parse_response() raises exception on non-200 status code"""
        # and puts the status code on the exception
        res = Mock(status_code=666)
        try:
            parse_response(res)
        except BasketException as e:
            self.assertEqual(666, e.status_code)
        else:
            self.fail("parse_response should have raised BasketException")

    def test_response_error(self):
        """parse_response() raises exception on status=error"""
        content = json.dumps({"status": "error", "desc": "ERROR", "code": 3})
        res = Mock(status_code=200, content=content, content_type="application/json")
        try:
            parse_response(res)
        except BasketException as e:
            self.assertEqual(3, e.code)
        else:
            self.fail("parse_response should have raised BasketException")

    def test_response_error_no_code(self):
        """if response has no code, and is error, then the code in
        the exception is the UNKNOWN code"""
        content = json.dumps({"status": "error", "desc": "ERROR"})
        res = Mock(status_code=200, content=content, content_type="application/json")
        try:
            parse_response(res)
        except BasketException as e:
            self.assertEqual(errors.BASKET_UNKNOWN_ERROR, e.code)
        else:
            self.fail("parse_response should have raised BasketException")

    def test_response_content(self):
        """parse_response() returns parsed response content if no error"""
        data = {"status": "ok", "foo": "bar"}
        content = json.dumps(data)
        res = Mock(status_code=200, content=content, content_type="application/json")
        result = parse_response(res)
        self.assertEqual(data, result)

    def test_response_no_content_type(self):
        """parse_response() doesn't fail if the response is missing a content type"""
        # probably only an issue in testing, but still...
        data = {"status": "ok", "foo": "bar"}
        content = json.dumps(data)
        res = Mock(status_code=200, content=content)
        result = parse_response(res)
        self.assertEqual(data, result)

    def test_request(self):
        """
        request() calls requests.request() with the expected parms
        if everything is normal, and returns the expected result.
        """
        response_data = {"status": "ok", "foo": "bar"}
        action, method, token = "ACTION", "METHOD", "TOKEN"
        url = basket_url(action, token)
        with patch("basket.base.requests.request", autospec=True) as request_call:
            request_call.return_value = Mock(status_code=200, content=json.dumps(response_data), content_type="application/json")
            result = request(method, action, data="DATA", token=token, params="PARAMS")

        request_call.assert_called_with(method, url, data="DATA", params="PARAMS", headers=None, timeout=ANY)
        self.assertEqual(response_data, result)

    def test_request_newsletters_string(self):
        """
        If request is passed newsletters as a string, newsletters is passed
        along unaltered.
        """
        input_data = {"newsletters": "one,two"}
        action, method, token = "ACTION", "METHOD", "TOKEN"
        url = basket_url(action, token)
        content = {"one": 100, "two": 200}
        with patch("basket.base.requests.request", autospec=True) as request_call:
            request_call.return_value = Mock(status_code=200, content=json.dumps(content), content_type="application/json")
            result = request(method, action, data=input_data, token=token, params="PARAMS")

        request_call.assert_called_with(method, url, data=input_data, params="PARAMS", headers=None, timeout=ANY)
        self.assertEqual(content, result)

    def test_request_newsletters_non_string(self):
        """
        If request is passed newsletters as a non-string, newsletters is
        converted to a comma-separated string
        """
        response_data = {"status": "ok", "foo": "bar"}
        input_data = {"newsletters": ["one", "two"], "thing": 1}
        expected_input_data = input_data.copy()
        newsletters = ",".join(input_data["newsletters"])
        expected_input_data["newsletters"] = newsletters
        action, method, token = "ACTION", "METHOD", "TOKEN"
        url = basket_url(action, token)
        with patch("basket.base.requests.request", autospec=True) as request_call:
            request_call.return_value = Mock(status_code=200, content=json.dumps(response_data), content_type="application/json")
            result = request(method, action, data=input_data, token=token, params="PARAMS")

        request_call.assert_called_with(method, url, data=expected_input_data, params="PARAMS", headers=None, timeout=ANY)
        self.assertEqual(response_data, result)

    def test_request_conn_error(self):
        """
        If requests throws a ConnectionError, it's converted to
        a BasketException
        """
        input_data = {"newsletters": ["one", "two"], "thing": 1}
        expected_input_data = input_data.copy()
        newsletters = ",".join(input_data["newsletters"])
        expected_input_data["newsletters"] = newsletters
        action, method, token = "ACTION", "METHOD", "TOKEN"
        with patch("basket.base.requests.request", autospec=True) as request_call:
            request_call.side_effect = ConnectionError
            with self.assertRaises(BasketException):
                request(method, action, data=input_data, token=token, params="PARAMS")

    def test_request_timeout(self):
        """
        If requests times out, it's converted to
        a BasketException
        """
        input_data = {"newsletters": ["one", "two"], "thing": 1}
        expected_input_data = input_data.copy()
        newsletters = ",".join(input_data["newsletters"])
        expected_input_data["newsletters"] = newsletters
        action, method, token = "ACTION", "METHOD", "TOKEN"
        with patch("basket.base.requests.request", autospec=True) as request_call:
            request_call.side_effect = Timeout
            with self.assertRaises(BasketException):
                request(method, action, data=input_data, token=token, params="PARAMS")

    def test_subscribe(self):
        """
        subscribe calls request with the expected parms and returns the result
        """
        email = "user1@example.com"
        newsletters = ["news1", "news2"]
        kwargs = {
            "arg1": 100,
            "arg2": 200,
        }
        expected_kwargs = kwargs.copy()
        expected_kwargs["email"] = email
        expected_kwargs["newsletters"] = newsletters
        with patch("basket.base.request", autospec=True) as request_call:
            result = subscribe(email, newsletters, **kwargs)

        request_call.assert_called_with("post", "subscribe", data=expected_kwargs, headers={})
        self.assertEqual(request_call.return_value, result)

    def test_subscribe_sync_y_api_key_in_args(self):
        """
        subscribe calls request with the expected parms and returns the result
        when sync='Y', adds the API key from the args to the headers
        """
        api_key = "foo_bar"
        email = "user1@example.com"
        newsletters = ["news1", "news2"]
        kwargs = {
            "arg1": 100,
            "arg2": 200,
            "sync": "Y",
            "api_key": api_key,
        }
        expected_kwargs = kwargs.copy()
        expected_kwargs["email"] = email
        expected_kwargs["newsletters"] = newsletters
        del expected_kwargs["api_key"]
        with patch("basket.base.request", autospec=True) as request_call:
            result = subscribe(email, newsletters, **kwargs)

        request_call.assert_called_with("post", "subscribe", data=expected_kwargs, headers={"x-api-key": api_key})
        self.assertEqual(request_call.return_value, result)

    def test_subscribe_sync_y_api_key_not_in_args(self):
        """
        subscribe calls request with the expected parms and returns the result
        when sync='Y', adds the API key from the settings to the headers
        """
        api_key = "foo_bar"
        email = "user1@example.com"
        newsletters = ["news1", "news2"]
        kwargs = {
            "arg1": 100,
            "arg2": 200,
            "sync": "Y",
        }
        expected_kwargs = kwargs.copy()
        expected_kwargs["email"] = email
        expected_kwargs["newsletters"] = newsletters
        with patch("basket.base.request", autospec=True) as request_call:
            with patch("basket.base.BASKET_API_KEY", api_key):
                result = subscribe(email, newsletters, **kwargs)

        request_call.assert_called_with("post", "subscribe", data=expected_kwargs, headers={"x-api-key": api_key})
        self.assertEqual(request_call.return_value, result)

    def test_unsubscribe(self):
        """
        unsubscribe calls request with the expected parms, returns the result
        """
        email = "user1@example.com"
        newsletters = ["news1", "news2"]
        token = "TOKEN"
        optout = False
        expected_data = {
            "email": email,
            "newsletters": newsletters,
        }
        with patch("basket.base.request", autospec=True) as request_call:
            result = unsubscribe(token, email, newsletters, optout)

        request_call.assert_called_with("post", "unsubscribe", data=expected_data, token=token)
        self.assertEqual(request_call.return_value, result)

    def test_unsubscribe_optout(self):
        """
        unsubscribe calls request with the expected parms and returns the
        result. optout is passed if true, instead of newsletters.
        """
        email = "user1@example.com"
        newsletters = ["news1", "news2"]
        token = "TOKEN"
        optout = True
        expected_data = {"email": email, "optout": "Y"}
        with patch("basket.base.request", autospec=True) as request_call:
            result = unsubscribe(token, email, newsletters, optout)

        request_call.assert_called_with("post", "unsubscribe", data=expected_data, token=token)
        self.assertEqual(request_call.return_value, result)

    def test_unsubscribe_bad_args(self):
        """
        unsubscribe must be passed newsletters or optout, or it raises
        BasketException
        """
        email = "user1@example.com"
        newsletters = None
        token = "TOKEN"
        optout = None
        with patch("basket.base.request", autospec=True):
            with self.assertRaises(BasketException):
                unsubscribe(token, email, newsletters, optout)

    def test_user(self):
        """
        user passes the expected args to request() and returns the result.
        """
        token = "TOKEN"
        with patch("basket.base.request", autospec=True) as request_call:
            result = user(token)
        request_call.assert_called_with("get", "user", token=token)
        self.assertEqual(request_call.return_value, result)

    def test_update_user(self):
        """
        update_user passes the expected args to request(), returns the result.
        """
        token = "TOKEN"
        kwargs = {
            "one": 100,
            "two": 200,
        }
        with patch("basket.base.request", autospec=True) as request_call:
            result = update_user(token, **kwargs)
        request_call.assert_called_with("post", "user", data=kwargs, token=token)
        self.assertEqual(request_call.return_value, result)

    def test_get_newsletters(self):
        """
        get_newsletters passes the expected args to request() and returns
        the 'newsletters' part of what it returns
        """
        with patch("basket.base.request", autospec=True) as request_call:
            request_call.return_value = {"newsletters": "FOO BAR"}
            result = get_newsletters()
        request_call.assert_called_with("get", "news.newsletters")
        self.assertEqual("FOO BAR", result)

    def test_confirm(self):
        """
        confirm() passes the expected args to request, and returns the result.
        """
        token = "TOKEN"
        with patch("basket.base.request", autospec=True) as request_call:
            result = confirm(token)
        request_call.assert_called_with("post", "confirm", token=token)
        self.assertEqual(request_call.return_value, result)

    def test_send_recovery_email(self):
        """
        send_recovery_email() passes the expected args to request,
        and returns the result.
        """
        email = "dude@example.com"
        with patch("basket.base.request", autospec=True) as mock_request:
            result = send_recovery_message(email)
        data = {"email": email}
        mock_request.assert_called_with("post", "recover", data=data)
        self.assertEqual(mock_request.return_value, result)

    @patch("basket.base.request")
    def test_lookup_user_token(self, mock_request):
        """Calling lookup_user with a token should not require an API key."""
        lookup_user(token="TOKEN")
        mock_request.assert_called_with("get", "users.lookup", params={"token": "TOKEN"})

    @patch("basket.base.request")
    def test_lookup_user_email(self, mock_request):
        """Calling lookup_user with email and api key should succeed."""
        api_key = "There is only XUL!"
        email = "dana@example.com"
        lookup_user(email=email, api_key=api_key)
        mock_request.assert_called_with("get", "users.lookup", params={"email": email}, headers={"x-api-key": api_key})

    @patch("basket.base.request")
    def test_lookup_user_email_setting(self, mock_request):
        """Calling lookup_user with email and api key setting should succeed."""
        api_key = "There is only XUL!"
        email = "dana@example.com"
        with patch("basket.base.BASKET_API_KEY", api_key):
            lookup_user(email=email)
        mock_request.assert_called_with("get", "users.lookup", params={"email": email}, headers={"x-api-key": api_key})

    @patch("basket.base.request")
    def test_lookup_user_no_api_key(self, mock_request):
        """Calling lookup_user with email and no api key raises an exception."""
        with self.assertRaises(BasketException):
            lookup_user(email="dana@example.com")

        self.assertFalse(mock_request.called)

    @patch("basket.base.request")
    def test_lookup_user_no_args(self, mock_request):
        """Calling lookup_user with no email or token raises an exception."""
        with self.assertRaises(BasketException):
            lookup_user()

        self.assertFalse(mock_request.called)

    @patch("basket.base.settings", type("X", (object,), {"TESTING_SETTINGS": True}))
    def test_gets_setting(self):
        """Should return the setting if it exists."""
        self.assertEqual(get_env_or_setting("TESTING_SETTINGS"), True)
        self.assertEqual(get_env_or_setting("DOES_NOT_EXIST"), None)

    def test_get_setting_from_env(self):
        """Should always return the value from the env if it exists."""
        self.assertEqual(get_env_or_setting("TESTING_SETTINGS"), None)
        with patch("basket.base.settings", type("X", (object,), {"TESTING_SETTINGS": "DUDE"})):
            self.assertEqual(get_env_or_setting("TESTING_SETTINGS"), "DUDE")
            with patch.dict("os.environ", {"TESTING_SETTINGS": "WALTER"}):
                self.assertEqual(get_env_or_setting("TESTING_SETTINGS"), "WALTER")

    @patch("basket.base.request")
    def test_subscribe_source_ip(self, mock_request):
        subscribe("dude@example.com", "abiding-times", source_ip="1.1.1.1")
        mock_request.assert_called_with(
            "post", "subscribe", data={"email": "dude@example.com", "newsletters": "abiding-times"}, headers={"x-source-ip": "1.1.1.1"}
        )

    @patch("basket.base.requests")
    def test_mock_success(self, mock_requests):
        result = subscribe("success@example.com", "abiding-times")
        self.assertEqual(result, {"status": "ok"})
        self.assertFalse(mock_requests.request.called)

    @patch("basket.base.requests")
    def test_mock_failure(self, mock_requests):
        with self.assertRaises(BasketException) as exc:
            subscribe("failure@example.com", "abiding-times")
        self.assertEqual(exc.exception.code, errors.BASKET_MOCK_FAILURE)
        self.assertFalse(mock_requests.request.called)
