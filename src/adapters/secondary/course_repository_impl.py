from sqlalchemy.exc import IntegrityError
from typing import Optional

from sqlalchemy import select, Select
from sqlalchemy.orm import Session

from src.application.entities.course import Course
from src.application.exceptions import DuplicateException
from src.application.secondary_ports.course_repository import ICourseRepository


class CourseRepository(ICourseRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> Optional[Course]:
        return self.session.get(Course, id)

    def get_all_by_name_like(self, name: str) -> list[Course]:
        stmt = Select(Course).where(Course.name.contains(name))
        courses = list(self.session.scalars(stmt).all())
        return courses

    def get_all_by_professor_id(self, professor_id: int) -> list[Course]:
        stmt = select(Course).where(Course.professor_id == professor_id)
        courses = list(self.session.scalars(stmt).all())
        return courses

    def save(self, course: Course) -> int:
        self.session.add(course)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise DuplicateException("Course name needs to be unique")
        return course.id

    def update(self, updated_course: Course) -> bool:
        try:
            self.session.commit()
            return True
        except IntegrityError:
            raise DuplicateException("Course name needs to be unique")

    def delete(self, course: Course) -> None:
        self.session.delete(course)
        self.session.commit()
