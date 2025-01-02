from dataclasses import dataclass
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from src.domain.dto import LectureResponseDto
from src.domain.exceptions import InvalidInputException


@dataclass
class Lecture:
    course_id: int
    date: datetime.date
    id: int = None
    password_hash: str = None

    def __repr__(self):
        return f"<Lecture {self.id} of {self.date}>"

    def __hash__(self):
        return hash((self.id, self.date, self.course_id))

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dto(self) -> LectureResponseDto:
        return LectureResponseDto(
            id=self.id,
            date=self.date,
        )

    @classmethod
    def factory(cls, course_id: int, date: str) -> "Lecture":
        try:
            parsed_date = datetime.strptime(date, '%Y-%m-%d').date()
        except:
            raise InvalidInputException("Date needs to be valid and of format YYYY-MM-DD!")
        return cls(course_id=course_id, date=parsed_date)
