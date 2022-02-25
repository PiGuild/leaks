from base64 import b64encode

from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher.PKCS1_v1_5 import PKCS115_Cipher
from Crypto.PublicKey import RSA


class Cryptogram:
    RSA_PUBLIC_KEY = (
        "-----BEGIN PUBLIC KEY-----\n"
        + "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAjU/bq6YZD2H0DUhbtEBg\n"
        + "JIyiurM8eX3aH02/ZWr6VZ27WF93ylWC4cGAe50sSgiA8NCW0G/UL77kAkebJQrJ\n"
        + "jVdt7SvDypSPk1mXNK0i9cI9DrdmAHLGLlYJx7eeY6h4JShLhOBnKRghi0S4uL5N\n"
        + "L7W4OUgCeUlGWcmz8ssNEQ5w17rfUF9TxYEFVKFMGN/SSaYNUr4znGt2r97YPsPy\n"
        + "0Sk4dGHhMXr1QGR05UQeVuU43OuRAFxA71YbuCRUYg5ENwKM/1RnNcu8v7kXFA4L\n"
        + "qGV9AncHLIZEOqWgY+4balVXlKIcMVN6W+PXKJpowOyB9QIq1Ec3OMaJ3sGpOppx\n"
        + "KQIDAQAB\n"
        + "-----END PUBLIC KEY-----"
    )

    def __init__(self, number: str, month: int, year: int, cvv: str, pubid: str):
        self.number = number
        self.month, self.year = month, year
        self.cvv = cvv
        self.PUBLIC_ID = pubid

    def _create_cryptogram(self) -> str:
        expiration_date = self._number_to_even_string(
            self.year
        ) + self._number_to_even_string(self.month)
        data = "@".join([self.number, expiration_date, self.cvv, self.PUBLIC_ID])
        cipher = self.make_cipher()

        return b64encode(cipher.encrypt(data.encode())).decode()

    @staticmethod
    def _number_to_even_string(number: int) -> str:
        number = str(number)
        return number if len(number) % 2 == 0 else "0" + number

    def create_hex_packet_from_data(self) -> str:
        return self._create_hex_packet(
            [
                1,
                self.number[:6],
                self.number[-4:],
                self.year,
                self.month,
                2,
                self._create_cryptogram(),
            ]
        )

    def _create_hex_packet(self, data) -> str:
        packet = [
            self._number_to_even_string(entry) if isinstance(entry, int) else entry
            for entry in data
        ]
        return "".join(packet)

    def make_cipher(self) -> PKCS115_Cipher:
        key = RSA.importKey(self.RSA_PUBLIC_KEY)
        return PKCS1_v1_5.new(key)
