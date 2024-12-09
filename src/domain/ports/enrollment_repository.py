from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.enrollment import Enrollment


class IEnrollmentRepository(ABC):
    @abstractmethod
    def get_by_course_id_and_user_id(self, course_id: int, user_id: int) -> Optional[Enrollment]:
        pass
