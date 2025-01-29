from dependency_injector.wiring import Provide, inject
from flask import Blueprint, g, request, render_template_string, url_for, render_template

from src.adapters.primary.blueprint.login_wrapper import login_required
from src.adapters.primary.config.container import Container
from src.application.primary_ports.attendance_service import AttendanceService

attendance = Blueprint('attendance', __name__, template_folder="../templates", url_prefix="/attendance")


@attendance.post("")
@inject
@login_required()
def save(attendance_service: AttendanceService = Provide[Container.attendance_service]):
    lecture_id = request.values.get("lecture_id", type=int)
    course_student_id = request.values.get("course_student_id", type=int)
    attendance_service.save(g.user, lecture_id, course_student_id)
    attendanceBtn = render_template_string(
        "{% import 'reusable/attendanceBtn.html' as attendance %}"
        "{{ attendance.button(has_attended, lecture_id, course_student_id) }}",
        lecture_id=lecture_id, course_student_id=course_student_id, has_attended=True
    )
    return attendanceBtn


@attendance.delete("")
@inject
@login_required()
def delete(
        attendance_service: AttendanceService = Provide[Container.attendance_service]
):
    lecture_id = request.values.get("lecture_id", type=int)
    course_student_id = request.values.get("course_student_id", type=int)
    if not lecture_id or not course_student_id:
        return "Value 'lecture_id' and 'course_student_id' are required", 400
    attendance_service.delete(g.user, lecture_id, course_student_id)
    attendance_btn = render_template_string(
        "{% import 'reusable/attendanceBtn.html' as attendance %}"
        "{{ attendance.button(has_attended, lecture_id, course_student_id) }}",
        lecture_id=lecture_id, course_student_id=course_student_id, has_attended=False
    )
    return attendance_btn


@attendance.get("/qr")
@inject
@login_required()
def get_qr_code_string(attendance_service: AttendanceService = Provide[Container.attendance_service]):
    lecture_id = request.args.get("lecture_id", type=int)
    seconds = request.args.get('seconds', type=int)
    if not seconds or not lecture_id:
        return "Values 'lecture_id' and 'seconds' are required", 400
    encypted_expiration_time = attendance_service.generate_qr_code_string(g.user, lecture_id, seconds)
    qr_code_link = url_for("attendance.save_with_qr_code_string", qr_code_string=encypted_expiration_time)
    return qr_code_link, 200


@attendance.get("/qr/<qr_code_string>")
@inject
@login_required()
def save_with_qr_code_string(
        qr_code_string: str,
        attendance_service: AttendanceService = Provide[Container.attendance_service]
):
    attendance_service.save_with_qr_code_string(g.user, qr_code_string)
    return render_template("success.html")


@attendance.post("/password")
@inject
@login_required()
def save_with_password(attendance_service: AttendanceService = Provide[Container.attendance_service]):
    password = request.form.get("password")
    course_id = request.form.get("course_id", type=int)
    if not password or not course_id:
        return "Values 'password' and 'course_id' are required", 400
    attendance_service.save_with_password(g.user, course_id, password)
    return render_template("success.html")
