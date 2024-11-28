from abc import ABC, abstractmethod

from src.domain.entities.course import Course


class ICourseRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int):
        pass

    @abstractmethod
    def get_all_by_professor_id(self, professor_id: int):
        pass