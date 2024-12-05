from src.domain.entities.lecture import Lecture
from src.domain.exceptions import NotFoundException
from src.domain.ports.lecture_repository import ILectureRepository
from src.domain.services.authorizer_service import AuthorizerService


class LectureService:
    def __init__(self, repo: ILectureRepository, authorizer: AuthorizerService):
        self.repo = repo
        self.authorizer = authorizer

    def save(self, lecture: Lecture, professor_id: int) -> int:
        """Saves a lecture to the course."""

        self.authorizer.is_professor_of_course(professor_id, lecture.course_id)
        return self.repo.save(lecture, professor_id)

    def delete(self, id, course_id: int, professor_id: int) -> None:
        """Deletes a lecture of the course."""

        self.authorizer.is_professor_of_course(professor_id, course_id)
        deleted = self.repo.delete(id)
        if not deleted:
            raise NotFoundException(f"Couldn't delete lecture. Lecture with ID: {id} doesn't exist")
