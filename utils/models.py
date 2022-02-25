import string

from random import choices


class Card:
    __slots__ = ("card", "month", "year", "cvc")

    def __init__(self, card: str, month: int, year: int, cvc: str) -> None:
        self.card: str = card
        self.month: str = self._number_to_even_string(month)
        self.year: str = self._number_to_even_string(year)
        self.cvc: str = cvc

    @staticmethod
    def _number_to_even_string(number: int) -> str:
        number = str(number)
        return number if len(number) % 2 == 0 else "0" + number


class RandomAccount:
    __slots__ = ("email", "real_email", "password", "device_id")

    def __init__(self) -> None:
        self.email: str = (
            "".join(choices(string.hexdigits, k=10)) + "@gmail.com"
        )
        self.password: str = "".join(choices(string.hexdigits, k=10))
        self.device_id: str = "".join(
            choices(string.ascii_lowercase + string.digits, k=16)
        )
