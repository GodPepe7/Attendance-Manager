from dataclasses import dataclass, field

from src.application.entities.lecture import Lecture
from src.application.entities.role import Role
from src.application.entities.user import User, InvalidRoleException


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
        Adds if the lecture belongs to the same course that the student is part of.
        """
        if self.course_id != lecture.course_id:
            raise InvalidRoleException("Lecture does not belong to the same course as student")
        self.attended_lectures.add(lecture)

    def remove_lecture(self, lecture: Lecture) -> None:
        """
        Will remove if the student has the lecture attendend.
        """
        if lecture in self.attended_lectures:
            self.attended_lectures.remove(lecture)
        return

    @classmethod
    def factory(cls, student: User, course_id: int) -> "CourseStudent":
        if student.role != Role.STUDENT:
            raise InvalidRoleException("User needs to have role 'STUDENT'")
        return cls(student, course_id)
