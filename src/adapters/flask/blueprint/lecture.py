from datetime import datetime

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, request, g, url_for, redirect, Response

from src.adapters.flask.blueprint.login_wrapper import login_required
from src.adapters.flask.config.container import Container
from src.domain.dto import UpdateLectureRequestDto
from src.domain.entities.lecture import Lecture
from src.domain.services.lecture_service import LectureService

lecture = Blueprint('lecture', __name__, url_prefix="/courses/<int:course_id>/lectures")


@lecture.post("/")
@inject
@login_required()
def save(course_id: int, lecture_service: LectureService = Provide[Container.lecture_service]):
    date = request.form.get('lecture-date')
    new_lecture = Lecture.factory(course_id, date)
    lecture_service.save(g.user, new_lecture)
    return redirect(url_for('course.get_by_id', course_id=course_id))


@lecture.delete("/<int:lecture_id>")
@inject
@login_required()
def delete(course_id: int, lecture_id: int, lecture_service: LectureService = Provide[Container.lecture_service]):
    lecture_service.delete(g.user, course_id, lecture_id)
    response = Response("Deleted lecture")
    response.headers["HX-Location"] = url_for('course.get_by_id', course_id=course_id)
    return response


@lecture.put("/<int:lecture_id>")
@inject
@login_required()
def update(course_id: int, lecture_id: int, lecture_service: LectureService = Provide[Container.lecture_service]):
    new_date = request.form.get("date")
    try:
        parsed_date = datetime.strptime(new_date, "%Y-%m-%d")
        lecture_request_dto = UpdateLectureRequestDto(lecture_id, course_id, parsed_date)
        lecture_service.update(g.user, lecture_request_dto)
        response = Response("Updated lecture")
        response.headers["HX-Location"] = url_for('course.get_by_id', course_id=course_id)
        return response
    except ValueError:
        return "Invalid date", 400
