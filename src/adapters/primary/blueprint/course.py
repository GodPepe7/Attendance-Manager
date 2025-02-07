from dependency_injector.wiring import inject, Provide
from flask import Blueprint, render_template, g, request, redirect, url_for, Response, render_template_string

from src.adapters.primary.blueprint.login_wrapper import login_required
from src.adapters.primary.config.container import Container
from src.application.dto import UpdateCourseRequestDto
from src.application.entities.course import Course
from src.application.primary_ports.course_service import CourseService

course = Blueprint("course", __name__, url_prefix="/courses", template_folder="../templates")


@course.get("")
@inject
@login_required()
def index(course_service: CourseService = Provide[Container.course_service]):
    courses_dto = course_service.get_all_by_prof(g.user)
    return render_template("course.html", courses=courses_dto)


@course.get("/search")
@inject
@login_required()
def get_by_name(course_service: CourseService = Provide[Container.course_service]):
    search_string = request.args.get("search-string")
    if not search_string:
        return "search_string is required", 400
    courses = course_service.get_all_by_name_like(search_string)
    course_list = render_template_string(
        "{% from 'reusable/searchCourseList.html' import course_list %}"
        "{{ course_list(courses) }}",
        courses=courses
    )
    return course_list


@course.get("/<int:course_id>")
@inject
@login_required()
def get_by_id(course_id: int, course_service: CourseService = Provide[Container.course_service]):
    course_data = course_service.get_by_id(g.user, course_id)
    return render_template("attendance.html", course=course_data)


@course.post("")
@inject
@login_required()
def save(course_service: CourseService = Provide[Container.course_service]):
    name = request.form.get("name")
    new_course = Course.factory(name, g.user)
    course_service.save(g.user, new_course)
    return redirect(url_for("course.index"))


@course.patch("/<int:course_id>")
@inject
@login_required()
def update(course_id: int, course_service: CourseService = Provide[Container.course_service]):
    name = request.form.get("name")
    password = request.form.get("password")
    expiration_datetime = request.form.get("password_expiration_datetime")
    dto = UpdateCourseRequestDto.factory(course_id, name, password, expiration_datetime)
    ok = course_service.update(g.user, dto)
    if not ok:
        return "There was an error updating the password", 500
    if password and expiration_datetime:
        return "", 204
    response = Response("Set password")
    response.headers["HX-Location"] = url_for('course.index')
    return response


@course.delete("/<int:course_id>")
@inject
@login_required()
def delete(course_id: int, course_service: CourseService = Provide[Container.course_service]):
    course_service.delete(g.user, course_id)
    response = Response("Deleted course")
    response.headers["HX-Location"] = url_for('course.index')
    return response


# filter function used in jinja template
@course.app_template_filter("has_attended")
def has_attended(lecture_id: int, attended_lectures) -> bool:
    return any(lecture_id == lecture.id for lecture in attended_lectures)
