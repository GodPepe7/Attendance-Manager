from dataclasses import dataclass, field

from src.domain.dto import EnrollmentDto
from src.domain.entities.lecture import Lecture
from src.domain.entities.user import User


@dataclass
class Enrollment:
    student: User
    course_id: int
    attended_lectures: set[Lecture] = field(default_factory=set)
    id: int = None

    def __hash__(self):
        return hash((self.id, self.student, self.course_id))

    def to_dto(self):
        return EnrollmentDto(
            id=self.id,
            student=self.student.to_dto(),
            attended_lectures=[attended_lecture.to_dto() for attended_lecture in self.attended_lectures]
        )
