from merchants.startru import *
from utils.startru_utils import *

from utils.models import Card

startru = StartRu(proxy="")  # http://user:pass@ip:port - необходимы с ротацией.
account_token = startru.register_account()
print(startru.account.email, startru.account.password)
pay_data = {"url": "/billing/buy/68ec7991-be62-4014-9629-72e7d79a890b?apikey"
                   + "=Wx6K6FjTh8TaJRIeqLwc6RoTAR0xaaKP"}
session_pay = startru.get_session(account_token, pay_data["url"])
print(session_pay)
card = Card("4048415045312345", 2, 22, 111)
fakecardhash = "1adc37f3b8646426ebf7eccbf1c9c4cc"
auth_card = startru.auth_card(account_token, session_pay, fakecardhash)
print(auth_card)
session_auth = auth_card["parameters"]["session_id"]
cryptogram = get_cryptogram(card)
submit_pay = startru.submit_pay(account_token, session_auth, fakecardhash, cryptogram)
print(submit_pay)
startru.client.close()
