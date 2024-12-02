from flask import Blueprint, render_template, g

from src.adapters.flask.blueprint.auth import login_required
from src.adapters.flask.config.sqlalchemy import db_session
from src.adapters.repositories.course_repository_impl import CourseRepository
from src.domain.entities.role import Role
from src.domain.services.course_service import CourseService

course = Blueprint('course', __name__, url_prefix="/courses", template_folder="../templates")

course_repo = CourseRepository(session=db_session())
course_service = CourseService(course_repo)


@course.get("/")
@login_required(roles=[Role.PROFESSOR])
def index():
    prof_id = g.user.id
    courses = course_service.get_courses_by_prof_id(prof_id)
    courses = [{"id": c.id, "name": c.name, "amount_students": len(c.enrolled_students)} for c in courses]
    return render_template("course.html", courses=courses)


@course.get("/<int:id>/")
@login_required(roles=[Role.PROFESSOR])
def get_course_by_id(id: int):
    course_data = course_service.get_by_id(id)
    course_data.lectures.sort(key=lambda lecture: lecture.date)
    return render_template("attendance.html", course=course_data)


@course.app_template_filter("is_attended")
def is_attended(student_id, attended_students) -> bool:
    return any(student_id == student.id for student in attended_students)
