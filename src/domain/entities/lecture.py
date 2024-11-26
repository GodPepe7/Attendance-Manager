import datetime
from dataclasses import dataclass, field

from src.domain.entities.attendance import Attendance


@dataclass
class Lecture:
    id: int
    course_id: int
    date: datetime.date
    attendances: list[Attendance] = field(default_factory=list)