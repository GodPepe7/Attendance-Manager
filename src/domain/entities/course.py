from dataclasses import dataclass, field

from src.domain.dto import CourseDto
from src.domain.entities.course_student import CourseStudent
from src.domain.entities.lecture import Lecture
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import UnauthorizedException


@dataclass
class Course:
    name: str
    professor: User
    id: int = None
    lectures: set[Lecture] = field(default_factory=set)
    students: set[CourseStudent] = field(default_factory=set)

    def __repr__(self):
        return f"<Course {self.id} {self.name}>"

    def __hash__(self):
        return hash((self.name, self.id, self.professor))

    def to_dto(self) -> CourseDto:
        return CourseDto(
            id=self.id,
            name=self.name,
            professor=self.professor.to_dto(),
            lectures=[lecture.to_dto() for lecture in self.lectures],
            students=[enrollment.to_dto() for enrollment in self.students]
        )

    @classmethod
    def factory(cls, name: str, user: User) -> "Course":
        if user.role != Role.PROFESSOR:
            raise UnauthorizedException("Only a professor can do this action")
        return cls(name=name, professor=user)
