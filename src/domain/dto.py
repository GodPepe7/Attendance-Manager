from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class UserDto:
    id: int
    name: str


@dataclass(frozen=True)
class LectureDto:
    id: int
    date: datetime.date


@dataclass(frozen=True)
class EnrollmentDto:
    id: int
    student: UserDto
    attended_lectures: list[LectureDto]


@dataclass(frozen=True)
class CourseDto:
    id: int
    name: str
    professor: UserDto
    lectures: list[LectureDto]
    enrolled_students: list[EnrollmentDto] = field(compare=False)
