from dataclasses import dataclass

from src.domain.entities.user import User


@dataclass
class Enrollment:
    id: int
    student: User
