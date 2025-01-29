import datetime
from dataclasses import dataclass, field

from werkzeug.security import generate_password_hash, check_password_hash

from src.application.dto import CourseResponseDto
from src.application.entities.course_student import CourseStudent
from src.application.entities.lecture import Lecture
from src.application.entities.role import Role
from src.application.entities.user import User
from src.application.exceptions import UnauthorizedException, NoPasswordAndExpirationYetException


@dataclass
class Course:
    name: str
    professor: User
    id: int = None
    password_hash: str = None
    password_expiration_datetime: datetime = None
    lectures: set[Lecture] = field(default_factory=set)
    students: set[CourseStudent] = field(default_factory=set)

    def __repr__(self):
        return f"<Course {self.id} {self.name}>"

    def __hash__(self):
        return hash((self.name, self.id, self.professor))

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str, date_time: datetime) -> bool:
        if not self.password_hash or not self.password_expiration_datetime:
            raise NoPasswordAndExpirationYetException("The professor hasn't set a password or validity time yet")
        is_correct_password = check_password_hash(self.password_hash, password)
        is_still_valid = self.password_expiration_datetime >= date_time
        return is_correct_password and is_still_valid

    def to_dto(self) -> CourseResponseDto:
        return CourseResponseDto(
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
