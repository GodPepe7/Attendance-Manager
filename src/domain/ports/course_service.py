from src.domain.entities.course import Course
from src.domain.ports.course_repository import ICourseRepository


class CourseService:
    def __init__(self, repo: ICourseRepository):
        self.repo = repo

    def get_courses_by_prof_id(self, professor_id: int):
        return self.repo.get_all_by_professor_id(professor_id)

    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)