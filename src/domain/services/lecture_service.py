from src.domain.entities.lecture import Lecture
from src.domain.exceptions import NoCourseException
from src.domain.ports.lecture_repository import ILectureRepository


class LectureService:
    def __init__(self, repo: ILectureRepository):
        self.repo = repo

    def save(self, lecture: Lecture, professor_id: int) -> None:
        """Saves a lecture to the professor's course. If no course is found, or it doesn't belong to the professor, raises a NoCourseException"""

        result = self.repo.save_to_own_course(lecture=lecture, professor_id=professor_id)
        if not result:
            raise NoCourseException(
                f"Couldn't save lecture. Professor doesn't have a course with id: {lecture.course_id}")
