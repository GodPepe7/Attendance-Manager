from dependency_injector.wiring import Provide, inject
from flask import (request, Blueprint, g, session, url_for, render_template, redirect)

from src.adapters.primary.config.container import Container
from src.application.entities.role import Role
from src.application.entities.user import User
from src.application.primary_ports.user_service import UserService

auth = Blueprint('auth', __name__, url_prefix="/auth", template_folder="../templates")


def _get_fallback_page(user: User) -> str:
    match user.role:
        case Role.PROFESSOR:
            return url_for("course.index")
        case Role.ADMIN:
            return url_for("admin.get_professors")
        case Role.STUDENT:
            return url_for("student.index")


@auth.before_app_request
@inject
def load_logged_in_user(user_service: UserService = Provide[Container.user_service]):
    """If a admin id is stored in the session, load the admin object from
    the database into ``g.admin``."""
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        try:
            g.user = user_service.get_by_id(user_id)
            if g.user is None:  # User was deleted
                session.clear()  # Clear invalid session
        except Exception as e:
            session.clear()  # Reset session on error
            g.user = None


@auth.route("/login", methods=["GET", "POST"])
@inject
def login(user_service: UserService = Provide[Container.user_service]):
    if g.user is not None:
        return redirect(_get_fallback_page(g.user))

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = user_service.authenticate(email, password)
        session["user_id"] = user.id
        next_page = session.pop('next', _get_fallback_page(user))
        return redirect(next_page)

    return render_template("login.html")


@auth.get("/logout")
def logout():
    session.clear()
    return "", 200
