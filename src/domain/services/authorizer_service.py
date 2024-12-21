from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import UnauthorizedException, NotFoundException
from src.domain.ports.course_repository import ICourseRepository
from src.domain.ports.lecture_repository import ILectureRepository


class AuthorizerService:
    def __init__(self, course_repo: ICourseRepository, lecture_repo: ILectureRepository):
        self.course_repo = course_repo
        self.lecture_repo = lecture_repo

    @staticmethod
    def check_if_role(user, role: Role):
        if not user.role == role:
            raise UnauthorizedException(f"Only users with the role: '{role.value}' can do this action")

    def check_if_professor_of_course(self, user: User, course_id: int):
        """
        Checks if the user is the professor of the course and thus authorized.
        Will throw an UnauthorizedException otherwise
        """
        self.check_if_role(user, Role.PROFESSOR)
        course = self.course_repo.get_by_id(course_id)
        if not course:
            raise NotFoundException(f"Course with ID: {id} doesn't exist")
        is_course_professor = course.professor.id == user.id
        if not is_course_professor:
            raise UnauthorizedException(
                "Only the course professor is allowed to do this action!")

    def check_if_professor_of_lecture(self, user: User, course_id: int, lecture_id: int):
        """
        Checks if the user is the professor of the lecture's course and thus authorized.
        Will throw an UnauthorizedException otherwise
        """
        self.check_if_role(user, Role.PROFESSOR)
        lecture = self.lecture_repo.get_by_id(lecture_id)
        if not lecture:
            raise NotFoundException(
                f"Lecture with ID: '{lecture_id}' doesn't exist!")
        is_course_lecture = lecture and lecture.course_id == course_id
        if not is_course_lecture:
            raise NotFoundException(
                f"Lecture with ID '{lecture_id}' is not part of the course with ID: '{course_id}'!")
        self.check_if_professor_of_course(user, course_id)
