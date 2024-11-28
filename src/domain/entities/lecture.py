import datetime
from dataclasses import dataclass, field

from src.domain.dto import LectureDto
from src.domain.entities.user import User


@dataclass
class Lecture:
    id: int
    date: datetime.date
    attended_students: list[User] = field(default_factory=list)

    def __repr__(self):
        return f"<Lecture {self.id} of {self.date}>"

    def to_dto(self) -> LectureDto:
        return LectureDto(
            id=self.id,
            date=self.date,
            attended_students=[student.to_dto() for student in self.attended_students]
        )