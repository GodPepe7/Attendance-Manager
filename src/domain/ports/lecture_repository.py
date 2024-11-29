from abc import ABC, abstractmethod

from src.domain.entities.lecture import Lecture


class ILectureRepository(ABC):
    @abstractmethod
    def save(self, lecture: Lecture, professor_id: int) -> int:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
