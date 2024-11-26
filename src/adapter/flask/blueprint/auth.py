import functools

from flask import (request, Blueprint, jsonify, g, session, abort)

from src.adapter.db.user_repository_impl import UserRepository
from src.adapter.flask.config.sqlalchemy import db_session
from src.domain.entities.role import Role
from src.domain.entities.user import user_factory
from src.domain.ports.user_service import UserService

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")
repo = UserRepository(db_session())
user_service = UserService(repo)


def login_required(role: Role = None):
    """View decorator that blocks access to sites if not logged in."""
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None or (role and g.user.role != role):
                return "", 403
            return view(**kwargs)
        return wrapped_view
    return decorator


@auth_bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = user_service.get_by_id(user_id)


@auth_bp.post("/login")
def login():
    body = request.json
    email = body["email"]
    password = body["password"]
    try:
        user = user_service.authenticate(email, password)
        session.clear()
        session["user_id"] = user.id
        print(f"saved id: {user.id}")
        return "", 200
    except Exception as e:
        abort(400, description=e)


@auth_bp.get("/logout")
def logout():
    session.clear()
    return "", 200


@auth_bp.get("/")
@login_required(role=Role.PROFESSOR)
def get_users():
    user = g.user
    return user_service.get_all()


@auth_bp.get("/<int:id>/")
def get_user(id):
    return jsonify(user_service.get_by_id(id))


@auth_bp.post("/")
@login_required(role=Role.ADMIN)
def save_users():
    body = request.json
    id = body["id"]
    email = body["email"]
    name = body["name"]
    password = body["password"]
    role = body["role"]
    try:
        user = user_factory(id, name, email, password, role)
        user_service.create_user(user)
        return jsonify({"message": "User created"}), 201
    except Exception as e:
        abort(400, description=e)
