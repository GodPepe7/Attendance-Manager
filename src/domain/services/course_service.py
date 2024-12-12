from src.domain.dto import CourseDto
from src.domain.entities.course import Course
from src.domain.exceptions import NotFoundException, UnauthorizedException
from src.domain.ports.course_repository import ICourseRepository


class CourseService:
    def __init__(self, repo: ICourseRepository):
        self.repo = repo

    def get_courses_by_prof_id(self, professor_id: int) -> list[CourseDto]:
        courses = self.repo.get_all_by_professor_id(professor_id)
        course_dtos = [course.to_dto() for course in courses]
        return course_dtos

    def get_by_id(self, user_id: int, id: int) -> CourseDto:
        course = self.repo.get_by_id(id)
        if not course:
            raise NotFoundException(f"Course with ID: {id} doesn't exist")
        is_course_professor = course.professor.id == user_id
        if not is_course_professor:
            raise UnauthorizedException(f"Only the professor of course with ID: {id} is allowed to do this action")
        return course.to_dto()

    def save(self, course: Course) -> int:
        return self.repo.save(course)
