from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.adapter.flask.config.sqlalchemy import Enrollment, Attendance
from src.domain.entities.course import Course
from src.domain.entities.user import User
from src.domain.ports.course_repository import ICourseRepository


class CourseRepository(ICourseRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> Optional[Course]:
        course = self.session.get(Course, id)
        stmt = select(User).join(Enrollment.student).where(Enrollment.course_id == course.id)
        enrolled_students = self.session.scalars(stmt).all()
        course.students = enrolled_students
        for lecture in course.lectures:
            stmt2 = select(User).join(Attendance.student).where(Attendance.lecture_id == lecture.id)
            attended_students = list(self.session.scalars(stmt2).all())
            lecture.attended_students = attended_students
        return course

    def get_all_by_professor_id(self, professor_id: int) -> list[Course]:
        stmt = select(Course).join(Course.professor).where(Course.professor_id == professor_id)
        courses = list(self.session.scalars(stmt).all())
        for course in courses:
            stmt2 = select(User).join(Enrollment.student).where(Enrollment.course_id == course.id)
            students = self.session.scalars(stmt2).all()
            course.students = students
        return courses