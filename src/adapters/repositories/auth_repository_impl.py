from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.entities.course import Course
from src.domain.ports.auth_repository import IAuthRepository


class AuthRepository(IAuthRepository):
    def __init__(self, session: Session):
        self.session = session

    def is_course_professor(self, professor_id: int, course_id: int) -> bool:
        stmt = (select(Course.id)
                .where(Course.id == course_id)
                .where(Course.professor_id == professor_id))
        course: Optional[Course] = self.session.scalar(stmt)
        if course:
            return True
        else:
            return False

    def is_lecture_student(self, student_id: int, lecture_id: int) -> bool:
        pass
