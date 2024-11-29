from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.entities.course import Course
from src.domain.entities.lecture import Lecture
from src.domain.ports.lecture_repository import ILectureRepository


class LectureRepository(ILectureRepository):
    def __init__(self, session: Session):
        self.session = session

    def save_to_own_course(self, lecture: Lecture, professor_id: int) -> bool:
        stmt = (select(Course)
                .where(Course.id == lecture.course_id)
                .where(Course.professor_id == professor_id))
        course: Optional[Course] = self.session.scalar(stmt)
        if course:
            course.lectures.append(lecture)
            self.session.commit()
            return True
        else:
            return False
