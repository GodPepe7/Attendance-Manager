from datetime import datetime

from flask import Blueprint, g, request, render_template_string, url_for

from src.adapters.flask.blueprint.auth import login_required
from src.adapters.flask.config.sqlalchemy import db_session
from src.adapters.repositories.attendance_repository_impl import AttendanceRepository
from src.adapters.repositories.course_repository_impl import CourseRepository
from src.adapters.repositories.lecture_repository_impl import LectureRepository
from src.domain.entities.role import Role
from src.domain.services.attendance_service import AttendanceService, IdWrapper
from src.domain.services.authorizer_service import AuthorizerService
from src.domain.services.encryption_service import EncryptionService

attendance = Blueprint('attendance', __name__,
                       url_prefix="/courses/<int:course_id>/lectures/<int:lecture_id>/attendance")
session = db_session()
attendance_repo = AttendanceRepository(session=session)
course_repo = CourseRepository(session=session)
lecture_repo = LectureRepository(session=session)
authorizer = AuthorizerService(course_repo, lecture_repo)
encryption_service = EncryptionService(fernet_key=b'njox0E4EdV3zF3vP7E1LZ79tj9kM9BiX79W8pdfh7tg=')
attendance_service = AttendanceService(attendance_repo, authorizer, encryption_service)


@attendance.post("/<int:student_id>")
@login_required(roles=[Role.PROFESSOR])
def save(course_id: int, lecture_id: int, student_id: int):
    ids = IdWrapper(g.user.id, course_id, lecture_id)
    attendance_service.save(ids, student_id)
    attendance_endpoint = url_for("attendance.save", course_id=course_id, lecture_id=lecture_id, student_id=student_id)
    attendanceBtn = render_template_string(
        "{% import 'reusable/attendanceBtn.html' as attendance %}"
        "{{ attendance.button(has_attended, attendance_endpoint) }}",
        attendance_endpoint=attendance_endpoint, has_attended=True
    )
    return attendanceBtn


@attendance.delete("/<int:student_id>")
@login_required(roles=[Role.PROFESSOR])
def delete(course_id: int, lecture_id: int, student_id: int):
    ids = IdWrapper(g.user.id, course_id, lecture_id)
    attendance_service.delete(ids, student_id)
    attendance_endpoint = url_for("attendance.save", course_id=course_id, lecture_id=lecture_id, student_id=student_id)
    attendanceBtn = render_template_string(
        "{% import 'reusable/attendanceBtn.html' as attendance %}"
        "{{ attendance.button(has_attended, attendance_endpoint) }}",
        attendance_endpoint=attendance_endpoint, has_attended=False
    )
    return attendanceBtn


@attendance.get("/qr")
@login_required(roles=[Role.PROFESSOR])
def get_qr_code_string(course_id: int, lecture_id: int):
    seconds_string = request.args.get('seconds')
    if not seconds_string:
        return "Missing 'seconds' paremeter in URL", 400
    try:
        seconds = int(seconds_string)
        ids = IdWrapper(g.user.id, course_id, lecture_id)
        encypted_expiration_time = attendance_service.generate_qr_code_string(ids, seconds, datetime.now())
        qr_code_link = url_for("attendance.save_with_qr_code_string", course_id=course_id, lecture_id=lecture_id,
                               qr_code_string=encypted_expiration_time)
        return qr_code_link, 200
    except ValueError:
        return "'seconds' input needs to be a valid number", 400


@attendance.get("/qr/<qr_code_string>")
@login_required(roles=[Role.STUDENT])
def save_with_qr_code_string(course_id: int, lecture_id: int, qr_code_string: str):
    ids = IdWrapper(g.user.id, course_id, lecture_id)
    attendance_service.save_with_qr_code_string(ids, qr_code_string, datetime.now())
    return "", 204
