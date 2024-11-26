from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.entities.course import Course
from src.domain.ports.course_repository import ICourseRepository


class CourseRepository(ICourseRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> Optional[Course]:
        course = self.session.get(Course, id)
        return course

    def get_all_by_professor_id(self, professor_id: int) -> list[Course]:
        stmt = select(Course).join(Course.professor).where(Course.professor_id == professor_id)
        courses = list(self.session.scalars(stmt).all())
        return courses