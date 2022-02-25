import re

import httpx

from modules.exceptions import *
from utils.models import *


class StartRu:
    __slots__ = ("client", "account", "api_host",
                 "payment_host", "api_key", "temp_token")

    def __init__(self, proxy: str = None, client: httpx.Client = None):
        self.client = client or httpx
        if not client and proxy:
            self.client = httpx.Client(http2=True, proxies=proxy, timeout=60,
                                       transport=httpx.HTTPTransport(retries=5, verify=False))
        self.account = RandomAccount()
        self.api_host: str = "https://api.start.ru"
        self.payment_host: str = "https://payment.start.ru"
        self.api_key: str = "Wx6K6FjTh8TaJRIeqLwc6RoTAR0xaaKP"
        self.temp_token: str = self.get_temp_token()

    def get_temp_token(self) -> str:
        try:
            return self.client.post(
                self.api_host + "/auth/device/login",
                params={
                    "apikey": self.api_key,
                },
                json={"device_id": "android_chrome_1111111111",
                      "device_type": "tv",
                      "device_name": "google_android",
                      "traffic_source": None}
            ).json()["authentication_token"]
        except (Exception,):
            raise AuthError()

    def register_account(self) -> str:
        try:
            return self.client.post(
                self.api_host + "/v2/auth/email/register",
                headers={"auth_token": self.temp_token},
                params={
                    "apikey": self.api_key,
                },
                json={
                    "email": self.account.email,
                    "password": self.account.password,
                    "status_gdpr": False,
                }
            ).json()["authentication_token"]
        except (Exception,):
            raise AuthError()

    def get_pay_url(self, account_token: str) -> dict:
        try:
            return self.client.get(
                self.api_host + "/billing/subscriptions",
                headers={"authentication_token": account_token},
                params={
                    "apikey": self.api_key,
                }
            ).json()
        except (Exception,):
            raise GetPayUrlError()

    def get_session(self, account_token: str, url: str) -> str:
        try:
            data = self.client.get(
                self.api_host + url,
                headers={"authentication_token": account_token},
                params={
                    "apikey": self.api_key,
                }
            ).text
            return re.findall('session=(.*?)&', data)[0]
        except (Exception,):
            raise GetSessionError()

    def auth_card(self, account_token: str, session: str, cardhash: str):
        try:
            return self.client.post(
                self.payment_host + "/billing/cloudpayments/auth",
                headers={"authentication_token": account_token},
                params={
                    "apikey": self.api_key,
                },
                json={
                    "device_type": "tv",
                    "platform_id": "start",
                    "session": session,
                    "gateway": "cloudpayments",
                    "card_info_hash": cardhash,
                    "card_info_hash_mcf": cardhash,
                },
            ).json()
        except (Exception,):
            raise AuthCardError()

    def submit_pay(self, account_token: str, session: str, cardhash: str, cryptogram: str):
        try:
            return self.client.post(
                self.payment_host + "/billing/cloudpayments/charge",
                headers={"authentication_token": account_token},
                params={
                    "apikey": self.api_key,
                },
                json={
                    "card_info_hash": cardhash,
                    "card_info_hash_mcf": cardhash,
                    "session": session,
                    "cryptogram": cryptogram,
                    "name": "START.RU SUBSCRIBER",
                    "device_type": "tv",
                    "platform_id": "start",
                },
            ).json()
        except (Exception,):
            raise SubmitPayError()
