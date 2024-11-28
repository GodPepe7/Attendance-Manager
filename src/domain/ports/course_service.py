from typing import Optional

from src.domain.dto import CourseDto
from src.domain.ports.course_repository import ICourseRepository


class CourseService:
    def __init__(self, repo: ICourseRepository):
        self.repo = repo

    def get_courses_by_prof_id(self, professor_id: int) -> list[CourseDto]:
        courses = self.repo.get_all_by_professor_id(professor_id)
        course_dtos = [course.to_dto() for course in courses]
        return course_dtos

    def get_by_id(self, id: int) -> Optional[CourseDto]:
        course = self.repo.get_by_id(id)
        if course:
            return course.to_dto()
        return None
