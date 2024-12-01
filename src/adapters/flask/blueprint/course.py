from flask import Blueprint, jsonify, render_template, g

from src.adapters.flask.blueprint.auth import login_required
from src.adapters.flask.config.sqlalchemy import db_session
from src.adapters.repositories.course_repository_impl import CourseRepository
from src.domain.entities.role import Role
from src.domain.services.course_service import CourseService

course = Blueprint('course', __name__, url_prefix="/course", template_folder="../templates")

course_repo = CourseRepository(session=db_session())
course_service = CourseService(course_repo)


@course.get("/")
@login_required(roles=[Role.PROFESSOR])
def index():
    prof_id = g.user.id
    courses = course_service.get_courses_by_prof_id(prof_id)
    return render_template("course.html"), courses


@course.get("/<int:id>/")
@login_required(roles=[Role.PROFESSOR])
def get_course_by_id(id: int):
    course = course_service.get_by_id(id)
    return jsonify(course), 200
