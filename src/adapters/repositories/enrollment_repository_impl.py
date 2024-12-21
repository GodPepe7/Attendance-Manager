from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.entities.course import Course
from src.domain.entities.enrollment import Enrollment
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import NotFoundException
from src.domain.ports.enrollment_repository import IEnrollmentRepository


class EnrollmentRepository(IEnrollmentRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_course_id_and_student_id(self, course_id: int, student_id: int) -> Optional[Enrollment]:
        stmt = (select(Enrollment)
                .where(Enrollment.course_id == course_id, Enrollment.student_id == student_id))
        return self.session.execute(stmt).scalar()

    def save_by_course_id_and_student_id(self, course_id: int, student_id: int) -> Enrollment:
        """Raises NotFoundException if student or course doesn't exist"""

        user = self.session.get(User, student_id)
        course = self.session.get(Course, course_id)
        if not user or user.role != Role.STUDENT:
            raise NotFoundException(f"Student with ID: {student_id} doesn't exist")
        if not course:
            raise NotFoundException(f"Course with ID: {course_id} doesn't exist")
        new_enrollment = Enrollment(user, course_id)
        course.enrolled_students.add(new_enrollment)
        self.session.commit()
        self.session.refresh(new_enrollment)
        return new_enrollment
