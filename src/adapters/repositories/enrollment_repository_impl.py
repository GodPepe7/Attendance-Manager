from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.entities.enrollment import Enrollment
from src.domain.ports.enrollment_repository import IEnrollmentRepository


class EnrollmentRepository(IEnrollmentRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_course_id_and_user_id(self, course_id: int, user_id: int) -> Optional[Enrollment]:
        stmt = (select(Enrollment)
                .where(Enrollment.course_id == course_id)
                .where(Enrollment.student_id == user_id))
        enrollment = self.session.execute(stmt).scalar()
        return enrollment
