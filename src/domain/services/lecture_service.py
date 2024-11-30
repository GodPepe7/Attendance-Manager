from src.domain.entities.lecture import Lecture
from src.domain.exceptions import NotFoundException
from src.domain.ports.auth_repository import IAuthRepository
from src.domain.ports.lecture_repository import ILectureRepository


class LectureService:
    def __init__(self, repo: ILectureRepository, auth_repo: IAuthRepository):
        self.repo = repo
        self.auth_repo = auth_repo

    def save(self, lecture: Lecture, professor_id: int) -> int:
        """Saves a lecture to the professor's course. If no course is found,
        or it doesn't belong to the professor, raises a NoCourseException"""
        is_course_professor = self.auth_repo.is_course_professor(professor_id, lecture.course_id)
        if not is_course_professor:
            raise NotFoundException(
                f"Couldn't save lecture. Only allowed to save lectures to owned courses!")
        return self.repo.save(lecture, professor_id)

    def delete(self, id, course_id: int, professor_id: int) -> None:
        """Deletes a lecture of the professor's course. If no course is found raises
        a NoCourseException or if no lecture is found raises a NoLectureException"""
        is_course_professor = self.auth_repo.is_course_professor(professor_id, course_id)
        if not is_course_professor:
            raise NotFoundException(
                f"Couldn't delete lecture. Only allowed to delete of owned courses!")
        deleted = self.repo.delete(id)
        if not deleted:
            raise NotFoundException(f"Couldn't delete lecture. Lecture with ID: {id} doesn't exist")
