from src.domain.dto import CourseResponseDto, UpdateCoursePasswordRequestDto, CourseGetByNameReponseDto
from src.domain.entities.course import Course
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import InvalidInputException
from src.domain.ports.course_repository import ICourseRepository
from src.domain.authorizer_utils import AuthorizerUtils


class CourseService:
    def __init__(self, repo: ICourseRepository):
        self.repo = repo

    def get_courses_by_prof(self, user: User) -> list[CourseResponseDto]:
        AuthorizerUtils.check_if_role(user, Role.PROFESSOR)
        courses = self.repo.get_all_by_professor_id(user.id)
        course_dtos = [course.to_dto() for course in courses]
        return course_dtos

    def get_courses_by_name_like(self, name: str) -> list[CourseGetByNameReponseDto]:
        courses = self.repo.get_all_by_name_like(name)
        course_dtos = [CourseGetByNameReponseDto(course.id, course.name, course.professor.name) for course in courses]
        return course_dtos

    def get_by_id(self, user: User, course_id: int) -> CourseResponseDto:
        course = self.repo.get_by_id(course_id)
        AuthorizerUtils.check_if_professor_of_course(user, course)
        course_dtos = course.to_dto()
        course_dtos.lectures.sort(key=lambda lecture: lecture.date)
        course_dtos.students.sort(key=lambda enrollment: enrollment.student.name)
        return course_dtos

    def save(self, user: User, course: Course) -> int:
        AuthorizerUtils.check_if_role(user, Role.PROFESSOR)
        return self.repo.save(course)

    def update_password(self, user: User, update_password_dto: UpdateCoursePasswordRequestDto) -> bool:
        course = self.repo.get_by_id(update_password_dto.course_id)
        AuthorizerUtils.check_if_professor_of_course(user, course)
        course.set_password(update_password_dto.password)
        course.password_expiration_datetime = update_password_dto.password_validty_datetime
        return self.repo.update(course)
