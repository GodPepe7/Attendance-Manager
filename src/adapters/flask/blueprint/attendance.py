from datetime import datetime

from flask import Blueprint, g, request

from src.adapters.flask.blueprint.auth import login_required
from src.adapters.flask.config.sqlalchemy import db_session
from src.adapters.repositories.attendance_repository_impl import AttendanceRepository
from src.adapters.repositories.auth_repository_impl import AuthRepository
from src.domain.entities.role import Role
from src.domain.services.attendance_service import AttendanceService
from src.domain.services.encryption_service import EncryptionService

attendance_bp = Blueprint('attendance', __name__,
                          url_prefix="/course/<int:course_id>/lecture/<int:lecture_id>/attendance")

attendance_repo = AttendanceRepository(session=db_session())
auth_repo = AuthRepository(session=db_session())
encryption_key: bytes
encryption_service = EncryptionService(fernet_key=b'njox0E4EdV3zF3vP7E1LZ79tj9kM9BiX79W8pdfh7tg=')
attendance_service = AttendanceService(attendance_repo, auth_repo, encryption_service)


@attendance_bp.post("/<int:student_id>")
@login_required(roles=[Role.PROFESSOR])
def save(course_id: int, lecture_id: int, student_id: int):
    user_id = g.user.id
    attendance_service.save(user_id, lecture_id, course_id, student_id)
    return "", 204


@attendance_bp.delete("/<int:student_id>")
@login_required(roles=[Role.PROFESSOR])
def delete(course_id: int, lecture_id: int, student_id: int):
    prof_id = g.user.id
    attendance_service.delete(prof_id, lecture_id, course_id, student_id)
    return "", 204


@attendance_bp.get("/qr")
@login_required(roles=[Role.PROFESSOR])
def get_qr_code_string(course_id: int, lecture_id: int):
    prof_id = g.user.id
    seconds_string = request.args.get('seconds')
    if not seconds_string:
        return "Missing 'seconds' paremeter in URL", 400
    try:
        seconds = int(seconds_string)
        encypted_expiration_time = attendance_service.generate_qr_code_string(prof_id, course_id, seconds,
                                                                              datetime.now())
        qr_code_link = f"/course/{course_id}/lecture/{lecture_id}/attendance/student/{encypted_expiration_time}"
        return qr_code_link, 200
    except ValueError:
        return "'seconds' input needs to be valid number", 400


@attendance_bp.get("/qr/<qr_code_string>")
@login_required(roles=[Role.STUDENT])
def save_with_qr_code_string(course_id: int, lecture_id: int, qr_code_string: str):
    student_id = g.user.id
    attendance_service.save_with_qr_code_string(student_id, course_id, lecture_id, qr_code_string, datetime.now())
    return "", 204
