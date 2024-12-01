from dataclasses import dataclass, field

from src.domain.dto import CourseDto
from src.domain.entities.lecture import Lecture
from src.domain.entities.user import User


@dataclass
class Course:
    name: str
    professor: User
    id: int = None
    lectures: set[Lecture] = field(default_factory=set)
    enrolled_students: set[User] = field(default_factory=set)

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
            enrolled_students=[student.to_dto() for student in self.enrolled_students]
        )
