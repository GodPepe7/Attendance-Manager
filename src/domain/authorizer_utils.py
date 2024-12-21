from src.domain.entities.course import Course
from src.domain.entities.lecture import Lecture
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import UnauthorizedException, NotFoundException
from src.domain.ports.course_repository import ICourseRepository
from src.domain.ports.lecture_repository import ILectureRepository


class AuthorizerUtils:
    @staticmethod
    def check_if_role(user, role: Role):
        if not user.role == role:
            raise UnauthorizedException(f"Only users with the role: '{role.value}' can do this action")

    @staticmethod
    def check_if_professor_of_course(user: User, course: Course):
        """
        Checks if the user is the professor of the course and thus authorized.
        Will throw an UnauthorizedException otherwise
        """
        AuthorizerUtils.check_if_role(user, Role.PROFESSOR)
        if not course:
            raise NotFoundException(f"Course doesn't exist")
        is_course_professor = course.professor.id == user.id
        if not is_course_professor:
            raise UnauthorizedException(
                "Only the course professor is allowed to do this action!")

    @staticmethod
    def check_if_professor_of_lecture(user: User, course: Course, lecture: Lecture):
        """
        Checks if the user is the professor of the lecture's course and thus authorized.
        Will throw an UnauthorizedException otherwise
        """
        AuthorizerUtils.check_if_role(user, Role.PROFESSOR)
        if not lecture:
            raise NotFoundException("Lecture doesn't exist!")
        if lecture.course_id != course.id:
            raise NotFoundException(
                f"Lecture with ID '{lecture.id}' is not part of the course with ID: '{course.id}'!")
        AuthorizerUtils.check_if_professor_of_course(user, course)
