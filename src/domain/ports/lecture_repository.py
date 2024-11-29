from abc import ABC, abstractmethod

from src.domain.entities.lecture import Lecture


class ILectureRepository(ABC):
    @abstractmethod
    def save_to_own_course(self, lecture: Lecture, professor_id: int) -> bool:
        pass
