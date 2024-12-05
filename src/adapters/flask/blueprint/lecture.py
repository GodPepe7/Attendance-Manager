from datetime import datetime

from flask import Blueprint, request, g, url_for, redirect

from src.adapters.flask.blueprint.auth import login_required
from src.adapters.flask.config.sqlalchemy import db_session
from src.adapters.repositories.course_repository_impl import CourseRepository
from src.adapters.repositories.lecture_repository_impl import LectureRepository
from src.domain.entities.lecture import Lecture
from src.domain.entities.role import Role
from src.domain.services.authorizer_service import AuthorizerService
from src.domain.services.lecture_service import LectureService

lecture = Blueprint('lecture', __name__, url_prefix="/courses/<int:course_id>/lectures")
session = db_session()
lecture_repo = LectureRepository(session=session)
course_repo = CourseRepository(session=session)
authorizer = AuthorizerService(course_repo, lecture_repo)
lecture_service = LectureService(lecture_repo, authorizer)


@lecture.post("/")
@login_required(roles=[Role.PROFESSOR])
def save(course_id: int):
    prof_id = g.user.id
    date = request.form.get('lecture-date')
    datetime.strptime(date, '%Y-%m-%d')
    lecture_data = Lecture.create(course_id=course_id, date=date)
    lecture_service.save(lecture=lecture_data, professor_id=prof_id)
    return redirect(url_for('course.get_by_id', course_id=course_id))


@lecture.delete("/<int:lecture_id>")
@login_required(roles=[Role.PROFESSOR])
def delete(course_id: int, lecture_id: int):
    prof_id = g.user.id
    lecture_service.delete(id=lecture_id, professor_id=prof_id, course_id=course_id)
    return "", 204
