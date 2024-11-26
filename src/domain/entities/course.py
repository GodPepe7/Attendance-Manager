from dataclasses import dataclass

from src.domain.entities.lecture import Lecture
from src.domain.entities.user import User


@dataclass
class Course:
    id: int
    name: str
    professor: User
    students: list[User]
    lectures: list[Lecture]