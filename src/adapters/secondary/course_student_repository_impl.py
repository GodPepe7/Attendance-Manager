from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.application.entities.course_student import CourseStudent
from src.application.secondary_ports.course_student_repository import ICourseStudentRepository


class CourseStudentRepository(ICourseStudentRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, course_student_id: int) -> Optional[CourseStudent]:
        return self.session.get(CourseStudent, course_student_id)

    def get_by_course_id_and_student_id(self, course_id: int, student_id: int) -> Optional[CourseStudent]:
        stmt = (select(CourseStudent)
                .where(CourseStudent.course_id == course_id, CourseStudent.student_id == student_id))
        return self.session.execute(stmt).scalar()

    def save(self, course_student: CourseStudent) -> int:
        self.session.add(course_student)
        self.session.commit()
        return course_student.id

    def update(self, course_student: CourseStudent) -> None:
        self.session.commit()
