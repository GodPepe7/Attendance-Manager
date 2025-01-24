from datetime import datetime

from src.domain.ports.clock import IClock


class Clock(IClock):
    def get_current_datetime(self) -> datetime:
        return datetime.now()
