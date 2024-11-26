from dataclasses import dataclass

from src.domain.entities.user import User


@dataclass
class Attendance:
    id: int
    student: User
