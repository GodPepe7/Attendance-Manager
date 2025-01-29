import datetime
from typing import Optional

from sqlalchemy import Select
from sqlalchemy.orm import Session

from src.application.entities.lecture import Lecture
from src.application.secondary_ports.lecture_repository import ILectureRepository


class LectureRepository(ILectureRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, lecture_id: int) -> Optional[Lecture]:
        return self.session.get(Lecture, lecture_id)

    def get_by_course_id_and_date(self, course_id: int, date: datetime.date) -> Optional[Lecture]:
        stmt = Select(Lecture).where(Lecture.course_id == course_id, Lecture.date == date)
        return self.session.scalar(stmt)

    def save(self, lecture: Lecture) -> int:
        self.session.add(lecture)
        self.session.commit()
        return lecture.id

    def delete(self, lecture: Lecture) -> None:
        self.session.delete(lecture)
        self.session.commit()

    def update(self, lecture: Lecture) -> bool:
        try:
            self.session.commit()
            return True
        except Exception as e:
            return False
