from utils.cryptogram import *
from hashlib import md5


def get_cryptogram(cc):
    return Cryptogram(
        cc.card, str(cc.month), str(cc.year), str(cc.cvc), "pk_ca68a63227e248e24c3be06dd9676"
    ).create_hex_packet_from_data()


def get_card_hash(cc):
    return md5(f"{cc.card}{cc.month}{cc.year}".encode()).hexdigest()
