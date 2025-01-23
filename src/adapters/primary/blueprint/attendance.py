from datetime import datetime

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, g, request, render_template_string, url_for, render_template

from src.adapters.primary.blueprint.login_wrapper import login_required
from src.adapters.primary.config.container import Container
from src.domain.services.attendance_service import AttendanceService

attendance = Blueprint('attendance', __name__, template_folder="../templates")


@attendance.post("/courses/<int:course_id>/lectures/<int:lecture_id>/attendance/<int:course_student_id>")
@inject
@login_required()
def save(
        course_id: int,
        lecture_id: int,
        course_student_id: int,
        attendance_service: AttendanceService = Provide[Container.attendance_service]
):
    attendance_service.save(g.user, course_id, lecture_id, course_student_id)
    delete_endpoint = url_for("attendance.delete", course_id=course_id, lecture_id=lecture_id,
                              course_student_id=course_student_id)
    attendanceBtn = render_template_string(
        "{% import 'reusable/attendanceBtn.html' as attendance %}"
        "{{ attendance.button(has_attended, attendance_endpoint) }}",
        attendance_endpoint=delete_endpoint, has_attended=True
    )
    return attendanceBtn


@attendance.delete("/courses/<int:course_id>/lectures/<int:lecture_id>/attendance/<int:course_student_id>")
@inject
@login_required()
def delete(
        course_id: int,
        lecture_id: int,
        course_student_id: int,
        attendance_service: AttendanceService = Provide[Container.attendance_service]
):
    attendance_service.delete(g.user, course_id, lecture_id, course_student_id)
    save_endpoint = url_for("attendance.save", course_id=course_id, lecture_id=lecture_id,
                            course_student_id=course_student_id)
    attendanceBtn = render_template_string(
        "{% import 'reusable/attendanceBtn.html' as attendance %}"
        "{{ attendance.button(has_attended, attendance_endpoint) }}",
        attendance_endpoint=save_endpoint, has_attended=False
    )
    return attendanceBtn


@attendance.get("/courses/<int:course_id>/lectures/<int:lecture_id>/attendance/qr")
@inject
@login_required()
def get_qr_code_string(
        course_id: int,
        lecture_id: int,
        attendance_service: AttendanceService = Provide[Container.attendance_service]
):
    seconds = request.args.get('seconds', type=int)
    if not seconds:
        return "Missing 'seconds' paremeter in URL", 400
    encypted_expiration_time = attendance_service.generate_qr_code_string(
        g.user,
        course_id,
        lecture_id,
        seconds,
        datetime.now()
    )
    qr_code_link = url_for(
        "attendance.save_with_qr_code_string",
        qr_code_string=encypted_expiration_time
    )
    return qr_code_link, 200


@attendance.get("/attendance/qr/<qr_code_string>")
@inject
@login_required()
def save_with_qr_code_string(
        qr_code_string: str,
        attendance_service: AttendanceService = Provide[Container.attendance_service]
):
    attendance_service.save_with_qr_code_string(g.user, qr_code_string, datetime.now())
    return render_template("success.html")


@attendance.post("/attendance/password")
@inject
@login_required()
def save_with_password(attendance_service: AttendanceService = Provide[Container.attendance_service]):
    password = request.form.get("password")
    course_id = request.form.get("course_id", type=int)
    if not password or not course_id:
        return "Need password and lecture_id", 400
    attendance_service.save_with_password(g.user, course_id, password)
    return render_template("success.html")
