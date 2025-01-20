import re
from dataclasses import dataclass, field
from datetime import datetime

from src.domain.exceptions import InvalidInputException


@dataclass(frozen=True)
class UserResponseDto:
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
class LectureResponseDto:
    id: int
    date: datetime.date


@dataclass(frozen=True)
class UpdateLectureRequestDto:
    lecture_id: int
    course_id: int
    date: datetime.date


@dataclass(frozen=True)
class UpdateCoursePasswordRequestDto:
    course_id: int
    password: str
    password_validty_time: datetime

    @classmethod
    def factory(cls, course_id: int, password: str,
                password_expiration_datetime: str) -> "UpdateCoursePasswordRequestDto":
        try:
            parsed_expiration_datetime = datetime.fromisoformat(password_expiration_datetime)
            return cls(course_id, password, parsed_expiration_datetime)
        except ValueError:
            raise InvalidInputException("Datetime for password validity needs to be in any valid ISO 8601 format")


@dataclass(frozen=True)
class CourseStudentResponseDto:
    id: int
    student: UserResponseDto
    attended_lectures: list[LectureResponseDto]


@dataclass(frozen=True)
class CourseResponseDto:
    id: int
    name: str
    professor: UserResponseDto
    lectures: list[LectureResponseDto]
    students: list[CourseStudentResponseDto] = field(compare=False)
