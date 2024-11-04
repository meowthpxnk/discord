from redis import Redis

from .services import SessionService


class Redis(Redis):
    def __init__(self, *args, **kwargs) -> "Redis":
        self.session_service = SessionService(self)
        super().__init__(*args, **kwargs)
