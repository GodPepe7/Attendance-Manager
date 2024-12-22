from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.entities.course import Course
from src.domain.entities.course_student import CourseStudent
from src.domain.entities.user import User
from src.domain.exceptions import NotFoundException
from src.domain.ports.course_student_repository import ICourseStudentRepository


class CourseStudentRepository(ICourseStudentRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, enrollment_id: int) -> Optional[CourseStudent]:
        return self.session.get(CourseStudent, enrollment_id)

    def get_by_course_id_and_student_id(self, course_id: int, student_id: int) -> Optional[CourseStudent]:
        stmt = (select(CourseStudent)
                .where(CourseStudent.course_id == course_id, CourseStudent.student_id == student_id))
        return self.session.execute(stmt).scalar()

    def save_by_course_id_and_user_id(self, course_id: int, user_id: int) -> CourseStudent:
        """Raises NotFoundException if student or course doesn't exist"""

        user = self.session.get(User, user_id)
        course = self.session.get(Course, course_id)
        if not user:
            raise NotFoundException(f"User with ID: {user_id} doesn't exist")
        if not course:
            raise NotFoundException(f"Course with ID: {course_id} doesn't exist")
        new_enrollment = CourseStudent.factory(user, course_id)
        course.students.add(new_enrollment)
        self.session.commit()
        self.session.refresh(new_enrollment)
        return new_enrollment

    def update(self, enrollment: CourseStudent) -> None:
        self.session.commit()
