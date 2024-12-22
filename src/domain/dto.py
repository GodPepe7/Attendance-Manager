import re
from dataclasses import dataclass, field
from datetime import datetime

from src.domain.exceptions import InvalidInputException


@dataclass(frozen=True)
class UserDto:
    id: int
    name: str
    email: str

    @classmethod
    def factory(cls, user_id: int, name: str, email: str):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise InvalidInputException("Needs to be valid email")
        return cls(user_id, name, email)


@dataclass(frozen=True)
class LectureDto:
    id: int
    date: datetime.date


@dataclass(frozen=True)
class CourseStudentDto:
    id: int
    student: UserDto
    attended_lectures: list[LectureDto]


@dataclass(frozen=True)
class CourseDto:
    id: int
    name: str
    professor: UserDto
    lectures: list[LectureDto]
    students: list[CourseStudentDto] = field(compare=False)
