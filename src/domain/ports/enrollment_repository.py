from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.enrollment import Enrollment


class IEnrollmentRepository(ABC):
    @abstractmethod
    def get_by_id(self, enrollment_id: int) -> Optional[Enrollment]:
        pass

    @abstractmethod
    def get_by_course_id_and_student_id(self, course_id: int, student_id: int) -> Optional[Enrollment]:
        pass

    @abstractmethod
    def save_by_course_id_and_user_id(self, course_id: int, student_id: int) -> Enrollment:
        pass

    @abstractmethod
    def update(self, enrollment: Enrollment) -> None:
        pass
