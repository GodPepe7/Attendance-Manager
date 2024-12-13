from dependency_injector.wiring import inject, Provide
from flask import Blueprint, render_template, g

from src.adapters.flask.blueprint.login_wrapper import login_required
from src.adapters.flask.config.container import Container
from src.domain.services.course_service import CourseService

course = Blueprint('course', __name__, url_prefix="/courses", template_folder="../templates")


@course.get("/")
@inject
@login_required()
def index(course_service: CourseService = Provide[Container.course_service]):
    courses = course_service.get_courses_by_prof(g.user)
    courses = [{"id": c.id, "name": c.name, "amount_students": len(c.enrolled_students)} for c in courses]
    return render_template("course.html", courses=courses)


@course.get("/<int:course_id>/")
@inject
@login_required()
def get_by_id(course_id: int, course_service: CourseService = Provide[Container.course_service]):
    course_data = course_service.get_by_id(user=g.user, course_id=course_id)
    course_data.lectures.sort(key=lambda lecture: lecture.date)
    course_data.enrolled_students.sort(key=lambda enrollment: enrollment.student.name)
    return render_template("attendance.html", course=course_data)


# filter function used in jinja template
@course.app_template_filter("has_attended")
def has_attended(lecture_id: int, attended_lectures) -> bool:
    return any(lecture_id == lecture.id for lecture in attended_lectures)
