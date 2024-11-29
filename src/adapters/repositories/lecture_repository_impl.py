from sqlalchemy.orm import Session

from src.domain.entities.lecture import Lecture
from src.domain.ports.lecture_repository import ILectureRepository


class LectureRepository(ILectureRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, lecture: Lecture, professor_id: int) -> int:
        self.session.add(lecture)
        self.session.commit()
        return lecture.id

    def delete(self, id: int) -> bool:
        lecture = self.session.get(Lecture, id)
        if not lecture:
            return False
        self.session.delete(lecture)
        self.session.commit()
        return True
