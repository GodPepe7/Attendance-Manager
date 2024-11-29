from flask import Blueprint, g, jsonify, request

from src.adapters.flask.blueprint.auth import login_required
from src.adapters.flask.config.sqlalchemy import db_session
from src.adapters.repositories.course_repository_impl import CourseRepository
from src.adapters.repositories.lecture_repository_impl import LectureRepository
from src.domain.entities.lecture import Lecture
from src.domain.entities.role import Role
from src.domain.services.course_service import CourseService
from src.domain.services.lecture_service import LectureService

course_bp = Blueprint('course', __name__, url_prefix="/course")

course_repo = CourseRepository(session=db_session())
course_service = CourseService(course_repo)
lecture_repo = LectureRepository(session=db_session())
lecture_service = LectureService(lecture_repo)


@course_bp.get("/")
@login_required(role=Role.PROFESSOR)
def get_courses():
    prof_id = g.user.id
    courses = course_service.get_courses_by_prof_id(prof_id)
    return courses


@course_bp.get("/<int:id>/")
@login_required(role=Role.PROFESSOR)
def get_course_by_id(id: int):
    course = course_service.get_by_id(id)
    return jsonify(course), 200


@course_bp.post("/<int:course_id>/lecture")
@login_required(role=Role.PROFESSOR)
def save_course(course_id: int):
    body = request.json
    date = body["date"]
    lecture = Lecture.create(course_id=course_id, date=date)
    lecture_service.save(lecture)
    return "", 204
