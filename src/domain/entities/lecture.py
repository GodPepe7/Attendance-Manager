import datetime
from dataclasses import dataclass, field

from src.domain.entities.user import User


@dataclass
class Lecture:
    id: int
    course_id: int
    date: datetime.date
    attended_students: list[User] = field(default_factory=list)