from dataclasses import dataclass

from src.domain.dto import EnrollmentDto
from src.domain.entities.user import User


@dataclass
class Enrollment:
    student: User
    course_id: int
    id: int = None

    def __hash__(self):
        return hash((self.id, self.student, self.course_id))

    def to_dto(self):
        return EnrollmentDto(
            id=self.id,
            student=self.student.to_dto()
        )
