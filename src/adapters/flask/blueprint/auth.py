import functools

from flask import (request, Blueprint, jsonify, g, session, redirect, url_for, flash, render_template)

from src.adapters.flask.config.sqlalchemy import db_session
from src.adapters.repositories.user_repository_impl import UserRepository
from src.domain.entities.role import Role
from src.domain.entities.user import User
from src.domain.exceptions import InvalidCredentialsException
from src.domain.services.user_service import UserService

auth = Blueprint('auth', __name__, url_prefix="/auth", template_folder="../templates")
repo = UserRepository(db_session())
user_service = UserService(repo)


def login_required(roles: list[Role] = None):
    """View decorator that blocks access to sites if not logged in."""

    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                session['next'] = request.url
                return redirect(url_for('auth.login'))
            if roles and g.user.role not in roles:
                flash(f"Access denied. Required roles: {[role.name for role in roles]}", 'error')
                return f"User needs to be logged in as {[role.name for role in roles]}!", 403
            return view(**kwargs)

        return wrapped_view

    return decorator


@auth.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = user_service.get_by_id(user_id)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if g.user is not None:
        return redirect(url_for("course.index"))

    if request.method == "POST":
        email = request.form.get('username')
        password = request.form.get('password')
        try:
            user = user_service.authenticate(email, password)
            session["user_id"] = user.id
            next_page = session.get('next')
            session.pop('next', None)
            return redirect(next_page or url_for('course.index'))
        except InvalidCredentialsException:
            flash(str(InvalidCredentialsException), "error")
            response = {"error": "InvalidCredentialsException", "message": str(InvalidCredentialsException)}
            return jsonify(response), 403

    return render_template("login.html")


@auth.get("/logout")
def logout():
    session.clear()
    return "", 200


@auth.get("/")
@login_required(roles=[Role.PROFESSOR])
def get_users():
    return user_service.get_all()


@auth.get("/<int:id>/")
def get_user(id):
    return jsonify(user_service.get_by_id(id))


@auth.post("/")
# @login_required(roles=[Role.ADMIN])
def save_users():
    body = request.json
    email = body["email"]
    name = body["name"]
    password = body["password"]
    role = body["role"]
    user = User.create(name, email, password, role)
    user_service.create_user(user)
    return jsonify({"message": "User created"}), 201
