from dependency_injector.wiring import Provide, inject
from flask import Blueprint, g, request, Response, url_for, render_template, jsonify

from src.adapters.primary.blueprint.login_wrapper import login_required
from src.adapters.primary.config.container import Container
from src.application.dto import UserResponseDto, UpdateUserRequestDto
from src.application.entities.user import User
from src.application.primary_ports.admin_service import AdminService
from src.application.primary_ports.user_service import UserService

user = Blueprint('user', __name__, url_prefix="/professors", template_folder="../templates")


@user.get("")
@inject
@login_required()
def get_professors(admin_service: AdminService = Provide[Container.admin_service]):
    all_professors = admin_service.get_all_professors(g.user)
    return render_template("admin.html", professors=all_professors)


@user.delete("/<int:user_id>")
@inject
@login_required()
def delete_professor(user_id: int, admin_service: AdminService = Provide[Container.admin_service]):
    admin_service.delete_professor(g.user, user_id)
    response = Response("Deleted professor")
    response.headers["HX-Location"] = url_for('user.get_professors')
    return response


@user.patch("/<int:user_id>")
@inject
@login_required()
def update_professor(user_id: int, admin_service: AdminService = Provide[Container.admin_service]):
    body = request.form
    email = body["email"]
    name = body["name"]
    user_dto = UpdateUserRequestDto.factory(user_id, name, email)
    admin_service.update_professor(g.user, user_dto)
    response = Response("Updated professor")
    response.headers["HX-Location"] = url_for('user.get_professors')
    return response


@user.post("")
@inject
@login_required()
def save_user(user_service: UserService = Provide[Container.user_service]):
    body = request.json
    email = body["email"]
    name = body["name"]
    password = body["password"]
    role = body["role"]
    new_user = User.factory(name, email, password, role)
    user_service.create_user(new_user)
    return jsonify({"message": "User created"}), 201
