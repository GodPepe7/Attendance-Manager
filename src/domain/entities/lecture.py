from dataclasses import dataclass
from datetime import datetime

from src.domain.dto import LectureResponseDto
from src.domain.exceptions import InvalidInputException


@dataclass
class Lecture:
    course_id: int
    date: datetime.date
    id: int = None

    def __repr__(self):
        return f"<Lecture {self.id} of {self.date}>"

    def __hash__(self):
        return hash((self.id, self.date, self.course_id))

    def to_dto(self) -> LectureResponseDto:
        return LectureResponseDto(
            id=self.id,
            date=self.date,
        )

    @classmethod
    def factory(cls, course_id: int, date: str) -> "Lecture":
        try:
            parsed_date = datetime.strptime(date, '%Y-%m-%d').date()
            return cls(course_id=course_id, date=parsed_date)
        except:
            raise InvalidInputException("Date needs to be valid and of format YYYY-MM-DD!")
