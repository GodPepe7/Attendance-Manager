import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

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
    date: datetime.date

    @classmethod
    def factory(cls, lecture_id: int, date_str: str) -> "UpdateLectureRequestDto":
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
            return cls(lecture_id, parsed_date)
        except ValueError:
            raise InvalidInputException("Date needs to be of format YYYY-MM-DD")


@dataclass(frozen=True)
class UpdateCourseRequestDto:
    course_id: int
    name: Optional[str]
    password: Optional[str]
    password_expiration_datetime: Optional[datetime]

    @classmethod
    def factory(cls, course_id: Optional[int], name: Optional[str], password: Optional[str],
                password_expiration_datetime: Optional[str]) -> "UpdateCourseRequestDto":
        if not name and not password and not password_expiration_datetime:
            raise InvalidInputException("Need at least one field")
        if (password and not password_expiration_datetime) or (not password and password_expiration_datetime):
            raise InvalidInputException(
                "For updating either password or password_expiration_datetime both are required")
        parsed_expiration_datetime = None
        try:
            if password_expiration_datetime:
                parsed_expiration_datetime = datetime.fromisoformat(password_expiration_datetime)
        except ValueError:
            raise InvalidInputException("Datetime for password validity needs to be in any valid ISO 8601 format")
        return cls(course_id, name, password, parsed_expiration_datetime)


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


@dataclass(frozen=True)
class CourseGetByNameReponseDto:
    id: int
    name: str
    professor_name: str
