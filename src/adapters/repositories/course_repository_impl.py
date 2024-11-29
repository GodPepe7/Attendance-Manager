from typing import Optional

from sqlalchemy import select, Select
from sqlalchemy.orm import Session, defaultload

from src.domain.entities.course import Course
from src.domain.entities.lecture import Lecture
from src.domain.entities.user import User
from src.domain.ports.course_repository import ICourseRepository


# query statement for course with only necessary data e.g. no password hash from user etc.
# due to lazyloading=select the not selected fields are only queried when accessed
def __select_course(self) -> Select[tuple[Course]]:
    template = (select(Course)
    .options(
        defaultload(Course.professor).load_only(User.id, User.name, raiseload=True),
        defaultload(Course.lectures).options(
            defaultload(Lecture.attended_students).load_only(User.id, User.name, raiseload=True))
    ))
    return template


class CourseRepository(ICourseRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> Optional[Course]:
        stmt = self.__select_course().where(Course.id == id)
        course = self.session.scalar(stmt)
        return course

    def get_all_by_professor_id(self, professor_id: int) -> list[Course]:
        stmt = self.__select_course().where(Course.professor_id == professor_id)
        courses = list(self.session.scalars(stmt).all())
        return courses
