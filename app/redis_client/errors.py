class NotValidPattern(Exception):
    def __init__(self, class_name: str) -> None:
        super().__init__(f"Not implemented pattern for class {class_name}")


class NotFoundInRedis(Exception):
    def __init__(self, class_name: str, id: str) -> None:
        return super().__init__(
            f"Not found in redis class {class_name}, id {id}"
        )
