from dataclasses import dataclass, field

from src.domain.dto import CourseStudentResponseDto
from src.domain.entities.lecture import Lecture
from src.domain.entities.role import Role
from src.domain.entities.user import User, InvalidRoleException
from src.domain.exceptions import NotFoundException


@dataclass
class CourseStudent:
    student: User
    course_id: int
    attended_lectures: set[Lecture] = field(default_factory=set)
    id: int = None

    def __hash__(self):
        return hash((self.id, self.student, self.course_id))

    def add_lecture(self, lecture: Lecture) -> None:
        """
        Will add to the CourseStudent if it's a course lecture.
        If a password is passed in, it will also check if it matches the lecture's password.
        """
        if self.course_id != lecture.course_id:
            raise NotFoundException("Lecture does not belong to the same course as student")
        self.attended_lectures.add(lecture)

    def to_dto(self):
        return CourseStudentResponseDto(
            id=self.id,
            student=self.student.to_dto(),
            attended_lectures=[attended_lecture.to_dto() for attended_lecture in self.attended_lectures]
        )

    @classmethod
    def factory(cls, student: User, course_id: int) -> "CourseStudent":
        if student.role != Role.STUDENT:
            raise InvalidRoleException("User needs to have role 'STUDENT'")
        return cls(student, course_id)
