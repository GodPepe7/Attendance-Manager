from src.domain.dto import UpdateLectureRequestDto
from src.domain.entities.lecture import Lecture
from src.domain.entities.user import User
from src.domain.ports.course_repository import ICourseRepository
from src.domain.ports.lecture_repository import ILectureRepository
from src.domain.authorizer_utils import AuthorizerUtils


class LectureService:
    def __init__(self, repo: ILectureRepository, course_repo: ICourseRepository):
        self.repo = repo
        self.course_repo = course_repo

    def save(self, user: User, lecture: Lecture) -> int:
        course = self.course_repo.get_by_id(lecture.course_id)
        AuthorizerUtils.check_if_professor_of_course(user, course)
        return self.repo.save(lecture)

    def delete(self, user: User, course_id: int, lecture_id: int) -> None:
        lecture = self.repo.get_by_id(lecture_id)
        course = self.course_repo.get_by_id(course_id)
        AuthorizerUtils.check_if_professor_of_lecture(user, course, lecture)
        self.repo.delete(lecture)

    def update(self, user: User, updated_lecture_dto: UpdateLectureRequestDto) -> None:
        lecture = self.repo.get_by_id(updated_lecture_dto.lecture_id)
        course = self.course_repo.get_by_id(updated_lecture_dto.course_id)
        AuthorizerUtils.check_if_professor_of_lecture(user, course, lecture)
        lecture.date = updated_lecture_dto.date
        if updated_lecture_dto.password:
            lecture.set_password(updated_lecture_dto.password)
        self.repo.update(lecture)
