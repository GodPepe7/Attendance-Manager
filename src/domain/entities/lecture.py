from dataclasses import dataclass, field
from datetime import datetime

from src.domain.dto import LectureDto
from src.domain.entities.user import User
from src.domain.exceptions import InvalidInputException


@dataclass
class Lecture:
    course_id: int
    date: datetime.date
    id: int = None
    attended_students: set[User] = field(default_factory=set)

    def __repr__(self):
        return f"<Lecture {self.id} of {self.date}>"

    def __hash__(self):
        return hash((self.id, self.date, self.course_id))

    def to_dto(self) -> LectureDto:
        return LectureDto(
            id=self.id,
            date=self.date,
            attended_students=[student.to_dto() for student in self.attended_students]
        )

    @classmethod
    def create(cls, course_id: int, date: str) -> "Lecture":
        try:
            parsed_date = datetime.strptime(date, '%Y-%m-%d').date()
        except:
            raise InvalidInputException("Date needs to be of format YYYY-MM-DD")
        return cls(course_id=course_id, date=parsed_date)
