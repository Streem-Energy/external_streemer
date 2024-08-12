from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import requests

from streemer.env import Env, ADMIN_EMAIL, ADMIN_PASSWORD

if TYPE_CHECKING:
    from typing import Optional


class RequestResultHandler:
    def handle(self, request):
        if request.ok:
            self.handle_success(request)
        else:
            self.handle_error(request)
        # TODO handle crash
        # also, use prepped request (see https://requests.readthedocs.io/en/latest/api/#requests.PreparedRequest)
        return request

    def handle_success(self, request):
        raise NotImplemented

    def handle_error(self, request):
        raise NotImplemented


class RequestResultQuiet(RequestResultHandler):
    def handle_success(self, request):  # TODO type
        print(request)

    def handle_error(self, request):
        print(request)


class RequestResultPrinter(RequestResultHandler):
    def handle_success(self, request):  # TODO type
        print(request)
        print(request.json())

    def handle_error(self, request):
        print(request)
        print(request.text)


@dataclass
class CsvRequestResultPrinter(RequestResultHandler):
    filename: Optional[str] = None

    def handle_success(self, request):
        print(request)
        print(request.text)

        if self.filename is not None:
            with open(self.filename, 'w') as f:
                f.write(request.text)

    def handle_error(self, request):
        print(request)  # TODO add color
        print(request.text)


@dataclass
class RequestsHandler:
    env: Env
    rrh: RequestResultHandler
    token: Optional[str] = None
    cookie: Optional[str] = None
    x_csrf_token: Optional[str] = None

    def authenticate(
            self,
            admin_email: Optional[str] = ADMIN_EMAIL,
            admin_password: Optional[str] = ADMIN_PASSWORD,
            client_email: Optional[str] = None
        ):
        params = {
            'email': admin_email,
            'password': admin_password,
        }
        if client_email is not None:
            params['client_email'] = client_email
            r = self.get('/admin_authenticate', params=params)
        else:
            r = self.post('/authenticate', params=params)

        self.token = r.json()['auth_token']

    def _form_headers(self, user_provided_headers: Optional[dict] = None):
        headers = user_provided_headers or {}
        headers['accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'
        if self.token is not None:
            headers['Authorization'] = self.token
        if self.cookie is not None:
            headers['Cookie'] = self.cookie
        if self.x_csrf_token is not None:
            headers['X-CSRF-Token'] = self.x_csrf_token
        return headers

    def get(self, route: str, params: Optional[dict] = None, headers: Optional[dict] = None):
        headers = self._form_headers(headers)
        url = self.env.base_url + route
        r = requests.get(url, params=params, headers=headers)
        return self.rrh.handle(r)

    def post(
        self,
        route: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        headers: Optional[dict] = None
    ):
        headers = self._form_headers(headers)
        url = self.env.base_url + route
        r = requests.post(url, params=params, data=data, json=json, headers=headers)
        return self.rrh.handle(r)

    def put(
        self,
        route: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        headers: Optional[dict] = None
    ):
        headers = self._form_headers(headers)
        url = self.env.base_url + route
        r = requests.put(url, params=params, data=data, headers=headers)
        return self.rrh.handle(r)
