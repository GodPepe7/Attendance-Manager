from src.domain.dto import CourseDto
from src.domain.entities.course import Course
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import NotFoundException, UnauthorizedException
from src.domain.ports.course_repository import ICourseRepository
from src.domain.services.authorizer_service import AuthorizerService


class CourseService:
    def __init__(self, repo: ICourseRepository, authorizer: AuthorizerService):
        self.repo = repo
        self.authorizer = authorizer

    def get_courses_by_prof(self, user: User) -> list[CourseDto]:
        self.authorizer.check_if_role(user, Role.PROFESSOR)
        courses = self.repo.get_all_by_professor_id(user.id)
        course_dtos = [course.to_dto() for course in courses]
        return course_dtos

    def get_by_id(self, user: User, course_id: int) -> CourseDto:
        self.authorizer.check_if_role(user, Role.PROFESSOR)
        course = self.repo.get_by_id(course_id)
        if not course:
            raise NotFoundException(f"Course with ID: {course_id} doesn't exist")
        is_course_professor = course.professor.id == user.id
        if not is_course_professor:
            raise UnauthorizedException(
                f"Only the professor of course with ID: {course_id} is allowed to do this action")
        return course.to_dto()

    def save(self, user: User, course: Course) -> int:
        self.authorizer.check_if_role(user, Role.PROFESSOR)
        return self.repo.save(course)
