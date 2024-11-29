from flask import Blueprint, request, g, jsonify

from src.adapters.flask.blueprint.auth import login_required
from src.adapters.flask.config.sqlalchemy import db_session
from src.adapters.repositories.auth_repository_impl import AuthRepository
from src.adapters.repositories.lecture_repository_impl import LectureRepository
from src.domain.entities.lecture import Lecture
from src.domain.entities.role import Role
from src.domain.services.lecture_service import LectureService

lecture_bp = Blueprint('lecture', __name__, url_prefix="/course/<int:course_id>/lecture")

lecture_repo = LectureRepository(session=db_session())
auth_repo = AuthRepository(session=db_session())
lecture_service = LectureService(lecture_repo, auth_repo)


@lecture_bp.post("/")
@login_required(role=Role.PROFESSOR)
def save(course_id: int):
    prof_id = g.user.id
    body = request.json
    date = body["date"]
    lecture = Lecture.create(course_id=course_id, date=date)
    id = lecture_service.save(lecture=lecture, professor_id=prof_id)
    response = {"id": id}
    return jsonify(response), 200


@lecture_bp.delete("/<int:lecture_id>")
@login_required(role=Role.PROFESSOR)
def delete(course_id: int, lecture_id: int):
    prof_id = g.user.id
    lecture_service.delete(id=lecture_id, professor_id=prof_id, course_id=course_id)
    return "", 204
