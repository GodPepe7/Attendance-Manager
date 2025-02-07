from dependency_injector.wiring import Provide, inject
from flask import Blueprint, g, request, Response, url_for, render_template, jsonify

from src.adapters.primary.blueprint.login_wrapper import login_required
from src.adapters.primary.config.container import Container
from src.application.dto import UpdateUserRequestDto
from src.application.entities.user import User
from src.application.primary_ports.user_service import UserService

admin = Blueprint('admin', __name__, url_prefix="/admin", template_folder="../templates")


@admin.get("")
@inject
@login_required()
def get_professors(user_service: UserService = Provide[Container.user_service]):
    all_professors = user_service.get_all_professors(g.user)
    return render_template("admin.html", professors=all_professors)


@admin.delete("/<int:user_id>")
@inject
@login_required()
def delete_professor(user_id: int, user_service: UserService = Provide[Container.user_service]):
    user_service.delete_professor(g.user, user_id)
    response = Response("Deleted professor")
    response.headers["HX-Location"] = url_for('admin.get_professors')
    return response


@admin.patch("/<int:user_id>")
@inject
@login_required()
def update_professor(user_id: int, user_service: UserService = Provide[Container.user_service]):
    body = request.form
    email = body["email"]
    name = body["name"]
    user_dto = UpdateUserRequestDto.factory(user_id, name, email)
    user_service.update_professor(g.user, user_dto)
    response = Response("Updated professor")
    response.headers["HX-Location"] = url_for('admin.get_professors')
    return response


@admin.post("")
@inject
@login_required()
def save_user(user_service: UserService = Provide[Container.user_service]):
    body = request.json
    email = body["email"]
    name = body["name"]
    password = body["password"]
    role = body["role"]
    new_user = User.factory(name, email, password, role)
    user_service.save(new_user)
    return jsonify({"message": "User created"}), 201
