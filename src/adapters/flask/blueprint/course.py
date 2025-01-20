from dependency_injector.wiring import inject, Provide
from flask import Blueprint, render_template, g, request, redirect, url_for, Response, render_template_string

from src.adapters.flask.blueprint.login_wrapper import login_required
from src.adapters.flask.config.container import Container
from src.domain.dto import UpdateCoursePasswordRequestDto
from src.domain.entities.course import Course
from src.domain.services.course_service import CourseService

course = Blueprint("course", __name__, url_prefix="/courses", template_folder="../templates")


@course.get("/")
@inject
@login_required()
def index(course_service: CourseService = Provide[Container.course_service]):
    courses = course_service.get_courses_by_prof(g.user)
    courses = [{"id": c.id, "name": c.name, "amount_students": len(c.students)} for c in courses]
    return render_template("course.html", courses=courses)


@course.get("/search")
@inject
@login_required()
def get_by_name(course_service: CourseService = Provide[Container.course_service]):
    search_string = request.args.get("search-string")
    if not search_string:
        return "search_string is required", 400
    courses = course_service.get_courses_by_name_like(search_string)
    course_list = render_template_string(
        "{% from 'reusable/searchCourseList.html' import course_list %}"
        "{{ course_list(courses) }}",
        courses=courses
    )
    return course_list


@course.get("/<int:course_id>/")
@inject
@login_required()
def get_by_id(course_id: int, course_service: CourseService = Provide[Container.course_service]):
    course_data = course_service.get_by_id(g.user, course_id)
    return render_template("attendance.html", course=course_data)


@course.post("/")
@inject
@login_required()
def save(course_service: CourseService = Provide[Container.course_service]):
    name = request.form.get("name")
    new_course = Course.factory(name, g.user)
    course_service.save(g.user, new_course)
    return redirect(url_for("course.index"))


@course.patch("/<int:course_id>/")
@inject
@login_required()
def update_password(course_id: int, course_service: CourseService = Provide[Container.course_service]):
    password = request.form.get("password")
    expiration_datetime = request.form.get("password_expiration_datetime")
    if not password or not expiration_datetime:
        return "Password and Password Validty Time are required", 400
    dto = UpdateCoursePasswordRequestDto.factory(course_id, password, expiration_datetime)
    ok = course_service.update_password(g.user, dto)
    if not ok:
        return "There was an error updating the password", 500
    return "", 204


# filter function used in jinja template
@course.app_template_filter("has_attended")
def has_attended(lecture_id: int, attended_lectures) -> bool:
    return any(lecture_id == lecture.id for lecture in attended_lectures)
