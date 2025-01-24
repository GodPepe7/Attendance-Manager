from abc import ABC, abstractmethod
from datetime import datetime


class IClock(ABC):
    @abstractmethod
    def get_current_datetime(self) -> datetime:
        pass
