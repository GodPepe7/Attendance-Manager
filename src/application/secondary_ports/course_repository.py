from abc import ABC, abstractmethod
from typing import Optional

from src.application.entities.course import Course


class ICourseRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Course]:
        pass

    @abstractmethod
    def get_all_by_name_like(self, name: str) -> list[Course]:
        pass

    @abstractmethod
    def get_all_by_professor_id(self, professor_id: int) -> list[Course]:
        pass

    @abstractmethod
    def save(self, course: Course) -> int:
        pass

    @abstractmethod
    def update(self, updated_course: Course) -> bool:
        pass

    @abstractmethod
    def delete(self, course: Course) -> None:
        pass
