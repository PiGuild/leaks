class AuthError(Exception):
    def __init__(self) -> None:
        super().__init__("Неудачная авторизация.")


class GetPayUrlError(Exception):
    def __init__(self) -> None:
        super().__init__("Неудачное получение url_pay.")


class GetSessionError(Exception):
    def __init__(self) -> None:
        super().__init__("Неудачное получение get_session.")


class AuthCardError(Exception):
    def __init__(self) -> None:
        super().__init__("Неудачное получение auth_card.")


class SubmitPayError(Exception):
    def __init__(self) -> None:
        super().__init__("Неудачное получение submit_pay.")
