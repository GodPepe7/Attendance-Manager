from datetime import datetime

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, request, g, url_for, redirect

from src.adapters.flask.blueprint.login_wrapper import login_required
from src.adapters.flask.config.container import Container
from src.domain.entities.lecture import Lecture
from src.domain.entities.role import Role
from src.domain.services.lecture_service import LectureService

lecture = Blueprint('lecture', __name__, url_prefix="/courses/<int:course_id>/lectures")


@lecture.post("/")
@inject
@login_required(roles=[Role.PROFESSOR])
def save(course_id: int, lecture_service: LectureService = Provide[Container.lecture_service]):
    prof_id = g.user.id
    date = request.form.get('lecture-date')
    datetime.strptime(date, '%Y-%m-%d')
    lecture_data = Lecture.factory(course_id=course_id, date=date)
    lecture_service.save(lecture=lecture_data, professor_id=prof_id)
    return redirect(url_for('course.get_by_id', course_id=course_id))


@lecture.delete("/<int:lecture_id>")
@inject
@login_required(roles=[Role.PROFESSOR])
def delete(course_id: int, lecture_id: int, lecture_service: LectureService = Provide[Container.lecture_service]):
    prof_id = g.user.id
    lecture_service.delete(id=lecture_id, professor_id=prof_id, course_id=course_id)
    return "", 204
