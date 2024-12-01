from sqlalchemy.orm import Session

from src.domain.entities.course import Course
from src.domain.ports.auth_repository import IAuthRepository


class AuthRepository(IAuthRepository):

    def __init__(self, session: Session):
        self.session = session

    def is_course_professor(self, professor_id: int, course_id: int) -> bool:
        course = self.session.get(Course, course_id)
        return course is not None and course.professor.id == professor_id

    def is_course_student(self, student_id: int, course_id: int) -> bool:
        course = self.session.get(Course, course_id)
        if not course:
            return False
        return student_id in [student.id for student in course.enrolled_students]
