from datetime import datetime

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, g, request, render_template_string, url_for

from src.adapters.flask.blueprint.login_wrapper import login_required
from src.adapters.flask.config.container import Container
from src.domain.entities.role import Role
from src.domain.services.attendance_service import IdWrapper, AttendanceService

attendance = Blueprint('attendance', __name__,
                       url_prefix="/courses/<int:course_id>/lectures/<int:lecture_id>/attendance")


@attendance.post("/<int:student_id>")
@inject
@login_required(roles=[Role.PROFESSOR])
def save(
        course_id: int,
        lecture_id: int,
        student_id: int,
        attendance_service: AttendanceService = Provide[Container.attendance_service]
):
    ids = IdWrapper(g.user.id, course_id, lecture_id)
    attendance_service.save(ids, student_id)
    delete_endpoint = url_for("attendance.delete", course_id=course_id, lecture_id=lecture_id,
                              student_id=student_id)
    attendanceBtn = render_template_string(
        "{% import 'reusable/attendanceBtn.html' as attendance %}"
        "{{ attendance.button(has_attended, attendance_endpoint) }}",
        attendance_endpoint=delete_endpoint, has_attended=True
    )
    return attendanceBtn


@attendance.delete("/<int:student_id>")
@inject
@login_required(roles=[Role.PROFESSOR])
def delete(
        course_id: int,
        lecture_id: int, student_id: int,
        attendance_service: AttendanceService = Provide[Container.attendance_service]
):
    ids = IdWrapper(g.user.id, course_id, lecture_id)
    attendance_service.delete(ids, student_id)
    save_endpoint = url_for("attendance.save", course_id=course_id, lecture_id=lecture_id, student_id=student_id)
    attendanceBtn = render_template_string(
        "{% import 'reusable/attendanceBtn.html' as attendance %}"
        "{{ attendance.button(has_attended, attendance_endpoint) }}",
        attendance_endpoint=save_endpoint, has_attended=False
    )
    return attendanceBtn


@attendance.get("/qr")
@inject
@login_required(roles=[Role.PROFESSOR])
def get_qr_code_string(
        course_id: int,
        lecture_id: int,
        attendance_service: AttendanceService = Provide[Container.attendance_service]
):
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
@inject
@login_required(roles=[Role.STUDENT])
def save_with_qr_code_string(
        course_id: int,
        lecture_id: int,
        qr_code_string: str,
        attendance_service: AttendanceService = Provide[Container.attendance_service]
):
    ids = IdWrapper(g.user.id, course_id, lecture_id)
    attendance_service.save_with_qr_code_string(ids, qr_code_string, datetime.now())
    # TODO: give some sort of success page
    return "", 204
