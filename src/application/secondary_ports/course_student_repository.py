from abc import ABC, abstractmethod
from typing import Optional

from src.application.entities.course_student import CourseStudent


class ICourseStudentRepository(ABC):
    @abstractmethod
    def get_by_id(self, enrollment_id: int) -> Optional[CourseStudent]:
        pass

    @abstractmethod
    def get_by_course_id_and_student_id(self, course_id: int, student_id: int) -> Optional[CourseStudent]:
        pass

    @abstractmethod
    def save(self, course_student: CourseStudent) -> CourseStudent:
        pass

    @abstractmethod
    def update(self, enrollment: CourseStudent) -> None:
        pass
