from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserDto:
    id: int
    name: str


@dataclass
class LectureDto:
    id: int
    date: datetime.date
    attended_students: list[UserDto]


@dataclass
class CourseDto:
    id: int
    name: str
    professor: UserDto
    lectures: list[LectureDto]
    enrolled_students: list[UserDto]
