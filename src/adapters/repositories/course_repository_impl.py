from typing import Optional

from sqlalchemy import select, false
from sqlalchemy.orm import Session

from src.domain.entities.course import Course
from src.domain.ports.course_repository import ICourseRepository


class CourseRepository(ICourseRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> Optional[Course]:
        return self.session.get(Course, id)

    def get_all_by_professor_id(self, professor_id: int) -> list[Course]:
        stmt = select(Course).where(Course.professor_id == professor_id)
        courses = list(self.session.scalars(stmt).all())
        return courses

    def save(self, course: Course) -> int:
        self.session.add(course)
        self.session.commit()
        return course.id

    def update(self, updated_course: Course) -> bool:
        try:
            self.session.commit()
            return True
        except Exception as e:
            return False
