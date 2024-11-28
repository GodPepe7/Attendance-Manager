from dataclasses import dataclass, field

from src.domain.entities.lecture import Lecture
from src.domain.entities.user import User


@dataclass
class Course:
    id: int
    name: str
    professor: User
    lectures: list[Lecture] = field(default_factory=list)
    enrolled_students: list[User] = field(default_factory=list)
