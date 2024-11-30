from flask import Blueprint, g

from src.adapters.flask.blueprint.auth import login_required
from src.adapters.flask.config.sqlalchemy import db_session
from src.adapters.repositories.attendance_repository_impl import AttendanceRepository
from src.adapters.repositories.auth_repository_impl import AuthRepository
from src.domain.entities.role import Role
from src.domain.services.attendance_service import AttendanceService

attendance_bp = Blueprint('attendance', __name__,
                          url_prefix="/course/<int:course_id>/lecture/<int:lecture_id>/attendance")

attendance_repo = AttendanceRepository(session=db_session())
auth_repo = AuthRepository(session=db_session())
attendance_service = AttendanceService(attendance_repo, auth_repo)


@attendance_bp.post("/<int:student_id>")
@login_required(roles=[Role.PROFESSOR])
def save(course_id: int, lecture_id: int, student_id: int):
    user_id = g.user.id
    attendance_service.save(user_id, lecture_id, course_id, student_id)
    return "", 204


@attendance_bp.delete("/<int:student_id>")
@login_required(roles=[Role.PROFESSOR, Role.STUDENT])
def delete(course_id: int, lecture_id: int, student_id: int):
    prof_id = g.user.id
    attendance_service.delete(prof_id, lecture_id, course_id, student_id)
    return "", 204
