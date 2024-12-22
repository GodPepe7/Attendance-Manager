from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.course_student import CourseStudent


class ICourseStudentRepository(ABC):
    @abstractmethod
    def get_by_id(self, enrollment_id: int) -> Optional[CourseStudent]:
        pass

    @abstractmethod
    def get_by_course_id_and_student_id(self, course_id: int, student_id: int) -> Optional[CourseStudent]:
        pass

    @abstractmethod
    def save_by_course_id_and_user_id(self, course_id: int, student_id: int) -> CourseStudent:
        pass

    @abstractmethod
    def update(self, enrollment: CourseStudent) -> None:
        pass
