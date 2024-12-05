from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.lecture import Lecture


class ILectureRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Lecture]:
        pass

    @abstractmethod
    def save(self, lecture: Lecture, professor_id: int) -> int:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
