from src.application.entities.course import Course
from src.application.entities.role import Role
from src.application.entities.user import User
from src.application.exceptions import UnauthorizedException, NotFoundException


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
        is_course_professor = course.professor == user
        if not is_course_professor:
            raise UnauthorizedException(
                "Only the course professor is allowed to do this action!")
