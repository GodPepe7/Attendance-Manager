from flask import Blueprint, render_template, g

from src.adapters.primary.blueprint.login_wrapper import login_required
from src.application.authorizer_utils import AuthorizerUtils
from src.application.entities.role import Role

student_bp = Blueprint('student', __name__, url_prefix="/student", template_folder="../templates")


@student_bp.get("")
@login_required()
def index():
    AuthorizerUtils.check_if_role(g.user, Role.STUDENT)
    return render_template("log_attendance.html")
