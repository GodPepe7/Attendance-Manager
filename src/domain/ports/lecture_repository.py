import datetime
from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.lecture import Lecture


class ILectureRepository(ABC):
    @abstractmethod
    def get_by_id(self, lecture_id: int) -> Optional[Lecture]:
        pass

    @abstractmethod
    def save(self, lecture: Lecture) -> int:
        pass

    @abstractmethod
    def delete(self, lecture_id: int) -> bool:
        pass

    @abstractmethod
    def update(self, lecture_id: int, new_date: datetime.date) -> bool:
        pass
