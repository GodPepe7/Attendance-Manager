from flask import Blueprint, render_template, g

from src.adapters.flask.blueprint.login_wrapper import login_required
from src.domain.authorizer_utils import AuthorizerUtils
from src.domain.entities.role import Role

student_bp = Blueprint('student', __name__, url_prefix="/student", template_folder="../templates")


@student_bp.get("/")
@login_required()
def index():
    AuthorizerUtils.check_if_role(g.user, Role.STUDENT)
    return render_template("log_attendance.html")
