from src.domain.exceptions import UnauthorizedException, NotFoundException
from src.domain.ports.course_repository import ICourseRepository
from src.domain.ports.lecture_repository import ILectureRepository


class AuthorizerService:
    def __init__(self, course_repo: ICourseRepository, lecture_repo: ILectureRepository):
        self.course_repo = course_repo
        self.lecture_repo = lecture_repo

    def is_professor_of_course(self, prof_id: int, course_id: int):
        """Checks if the professor is the professor of the course and thus authorized. Will throw an UnauthorizedException otherwise"""

        course = self.course_repo.get_by_id(course_id)
        is_course_professor = course is not None and course.professor.id == prof_id
        if not is_course_professor:
            raise UnauthorizedException(
                "Only the course professor is allowed to do this action!")

    def is_professor_of_lecture(self, prof_id: int, course_id: int, lecture_id: int):
        lecture = self.lecture_repo.get_by_id(lecture_id)
        is_course_lecture = lecture and lecture.course_id == course_id
        if not is_course_lecture:
            raise NotFoundException(
                f"Lecture with ID '{lecture_id}' is not part of the course with ID: '{course_id}'!")
        self.is_professor_of_course(prof_id, course_id)

    def is_course_student(self, student_id: int, course_id: int):
        """Checks if the student is enrolled in the course and thus authorized. Will throw an UnauthorizedException otherwise"""

        course = self.course_repo.get_by_id(course_id)
        is_course_student = course and student_id in [student.id for student in course.enrolled_students]
        if not is_course_student:
            raise UnauthorizedException(
                "Only an enrolled student of the course is allowed to do this action!")
