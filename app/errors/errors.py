class NotValidPassword(Exception):
    def __init__(self) -> None:
        super().__init__("Not valid password.")


class NotValidUsernameOrPassword(Exception):
    def __init__(self) -> None:
        super().__init__("Not valid username or password.")
