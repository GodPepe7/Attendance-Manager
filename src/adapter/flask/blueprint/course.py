from flask import Blueprint, g, jsonify

from src.adapter.db.course_repository_impl import CourseRepository
from src.adapter.flask.blueprint.auth import login_required
from src.adapter.flask.config.sqlalchemy import db_session
from src.domain.entities.role import Role
from src.domain.ports.course_service import CourseService

course_bp = Blueprint('course', __name__, url_prefix="/course")

course_repo = CourseRepository(session=db_session())
course_service = CourseService(course_repo)

@course_bp.get("/")
@login_required(role=Role.PROFESSOR)
def get_courses():
    prof_id = g.user.id
    courses = course_service.get_courses_by_prof_id(prof_id)
    return courses

@course_bp.get("/<int:id>/")
@login_required(role=Role.PROFESSOR)
def get_course_by_id(id):
    prof_id = g.user.id
    return jsonify(course_service.get_by_id(id))