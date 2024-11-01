from redis import Redis


class Redis(Redis):
    def __init__(self, *args, **kwargs) -> "Redis":
        super().__init__(*args, **kwargs)
