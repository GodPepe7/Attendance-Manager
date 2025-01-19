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
    def factory(cls, course_id: int, password: str, password_validity_time: str) -> "UpdateCoursePasswordRequestDto":
        try:
            parsed_validity_time = datetime.strptime(password_validity_time, "%Y-%M-%d %H:%M")
            return cls(course_id, password, parsed_validity_time)
        except ValueError as e:
            raise InvalidInputException("Datetime for password validity needs to be in format YYYY-MM-DD HH:MM")


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
