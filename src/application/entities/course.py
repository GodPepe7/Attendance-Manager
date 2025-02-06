import datetime
from dataclasses import dataclass, field

from werkzeug.security import generate_password_hash, check_password_hash

from src.application.entities.course_student import CourseStudent
from src.application.entities.lecture import Lecture
from src.application.entities.role import Role
from src.application.entities.user import User
from src.application.exceptions import NoPasswordAndExpirationYetException, InvalidInputException


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

    def set_password_and_expiration(self, password: str, expiration: datetime) -> None:
        self.password_hash = generate_password_hash(password)
        self.password_expiration_datetime = expiration

    def check_password(self, password: str, date_time: datetime) -> bool:
        if not self.password_hash or not self.password_expiration_datetime:
            raise NoPasswordAndExpirationYetException("The professor hasn't set a password or validity time yet")
        is_correct_password = check_password_hash(self.password_hash, password)
        is_still_valid = self.password_expiration_datetime >= date_time
        return is_correct_password and is_still_valid

    @classmethod
    def factory(cls, name: str, professor: User) -> "Course":
        if professor.role != Role.PROFESSOR:
            raise InvalidInputException("User needs to be of role professor")
        return cls(name=name, professor=professor)
