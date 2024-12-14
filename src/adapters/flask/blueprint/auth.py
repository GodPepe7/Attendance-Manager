from dependency_injector.wiring import Provide, inject
from flask import (request, Blueprint, jsonify, g, session, redirect, url_for, render_template, Response,
                   render_template_string)

from src.adapters.flask.blueprint.login_wrapper import login_required
from src.adapters.flask.config.container import Container
from src.domain.entities.user import User
from src.domain.exceptions import InvalidCredentialsException
from src.domain.services.user_service import UserService

auth = Blueprint('auth', __name__, url_prefix="/auth", template_folder="../templates")


@auth.before_app_request
@inject
def load_logged_in_user(user_service: UserService = Provide[Container.user_service]):
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = user_service.get_by_id(user_id)


@auth.route("/login", methods=["GET", "POST"])
@inject
def login(user_service: UserService = Provide[Container.user_service]):
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
            response = Response("Logged in")
            response.headers["HX-Redirect"] = next_page or url_for('course.index')
            return response
        except InvalidCredentialsException as e:
            return render_template_string(f"<p>{e}<p>")

    return render_template("login.html")


@auth.get("/logout")
def logout():
    session.clear()
    return "", 200


@auth.post("/")
@inject
# @login_required()
def save_user(user_service: UserService = Provide[Container.user_service]):
    body = request.json
    email = body["email"]
    name = body["name"]
    password = body["password"]
    role = body["role"]
    user = User.factory(name, email, password, role)
    user_service.create_user(user)
    return jsonify({"message": "User created"}), 201
