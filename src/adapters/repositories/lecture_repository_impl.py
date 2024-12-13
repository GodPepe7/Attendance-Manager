import datetime
from typing import Optional

from sqlalchemy.orm import Session

from src.domain.entities.lecture import Lecture
from src.domain.ports.lecture_repository import ILectureRepository


class LectureRepository(ILectureRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, lecture_id: int) -> Optional[Lecture]:
        return self.session.get(Lecture, lecture_id)

    def save(self, lecture: Lecture) -> int:
        self.session.add(lecture)
        self.session.commit()
        return lecture.id

    def delete(self, lecture_id: int) -> bool:
        lecture = self.session.get(Lecture, lecture_id)
        if not lecture:
            return False
        self.session.delete(lecture)
        self.session.commit()
        return True

    def update(self, lecture_id: int, new_date: datetime.date) -> bool:
        lecture = self.session.get(Lecture, lecture_id)
        if not lecture:
            return False
        lecture.date = new_date
        self.session.commit()
        return True
