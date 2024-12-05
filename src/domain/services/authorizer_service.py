from src.domain.exceptions import UnauthorizedException
from src.domain.ports.course_repository import ICourseRepository


class AuthorizerService:
    def __init__(self, repo: ICourseRepository):
        self.course_repo = repo

    def is_professor_of_course(self, prof_id: int, course_id: int):
        """Checks if the professor is the professor of the course and thus authorized. Will throw an UnauthorizedException otherwise"""

        course = self.course_repo.get_by_id(course_id)
        is_course_professor = course is not None and course.professor.id == prof_id
        if not is_course_professor:
            raise UnauthorizedException(
                "Only the professor of the course is allowed to do this action!")

    def is_course_student(self, student_id: int, course_id: int):
        """Checks if the student is enrolled in the course and thus authorized. Will throw an UnauthorizedException otherwise"""

        course = self.course_repo.get_by_id(course_id)
        is_course_student = course and student_id in [student.id for student in course.enrolled_students]
        if not is_course_student:
            raise UnauthorizedException(
                "Only an enrolled student of the course is allowed to do this action!")
