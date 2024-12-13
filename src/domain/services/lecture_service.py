import datetime

from src.domain.entities.lecture import Lecture
from src.domain.entities.user import User
from src.domain.exceptions import NotFoundException
from src.domain.ports.lecture_repository import ILectureRepository
from src.domain.services.authorizer_service import AuthorizerService


class LectureService:
    def __init__(self, repo: ILectureRepository, authorizer: AuthorizerService):
        self.repo = repo
        self.authorizer = authorizer

    def save(self, user: User, lecture: Lecture) -> int:
        """Saves a lecture to the course."""

        self.authorizer.check_if_professor_of_course(user, lecture.course_id)
        return self.repo.save(lecture)

    def delete(self, user: User, course_id: int, lecture_id: int) -> None:
        """Deletes a lecture of the course."""

        self.authorizer.check_if_professor_of_lecture(user, course_id, lecture_id)
        self.repo.delete(lecture_id)

    def update(self, user: User, course_id: int, lecture_id: int, new_date: datetime.date) -> None:
        """Updates a lecture of the course."""

        self.authorizer.check_if_professor_of_lecture(user, course_id, lecture_id)
        self.repo.update(lecture_id, new_date)
