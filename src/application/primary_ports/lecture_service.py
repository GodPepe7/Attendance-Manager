from src.application.dto import UpdateLectureRequestDto
from src.application.entities.lecture import Lecture
from src.application.entities.user import User
from src.application.exceptions import NotFoundException
from src.application.secondary_ports.course_repository import ICourseRepository
from src.application.secondary_ports.lecture_repository import ILectureRepository
from src.application.authorizer_utils import AuthorizerUtils


class LectureService:
    def __init__(self, repo: ILectureRepository, course_repo: ICourseRepository):
        self.repo = repo
        self.course_repo = course_repo

    def save(self, user: User, lecture: Lecture) -> int:
        course = self.course_repo.get_by_id(lecture.course_id)
        AuthorizerUtils.check_if_professor_of_course(user, course)
        return self.repo.save(lecture)

    def delete(self, user: User, lecture_id: int) -> None:
        lecture = self.repo.get_by_id(lecture_id)
        if not lecture:
            raise NotFoundException(f"Lecture with ID {lecture_id} doesn't exist")
        course = self.course_repo.get_by_id(lecture.course_id)
        AuthorizerUtils.check_if_professor_of_course(user, course)
        self.repo.delete(lecture)

    def update(self, user: User, updated_lecture_dto: UpdateLectureRequestDto) -> bool:
        lecture = self.repo.get_by_id(updated_lecture_dto.lecture_id)
        if not lecture:
            raise NotFoundException(f"Lecture with ID {updated_lecture_dto.lecture_id} doesn't exist")
        course = self.course_repo.get_by_id(lecture.course_id)
        AuthorizerUtils.check_if_professor_of_course(user, course)
        lecture.date = updated_lecture_dto.date
        return self.repo.update(lecture)
