from dependency_injector.wiring import Provide, inject
from flask import Blueprint, g, request, Response, url_for, render_template

from src.adapters.flask.blueprint.login_wrapper import login_required
from src.adapters.flask.config.container import Container
from src.domain.dto import UserDto
from src.domain.services.admin_service import AdminService

admin = Blueprint('admin', __name__, url_prefix="/professors", template_folder="../templates")


@admin.get("/")
@inject
@login_required()
def get_professors(admin_service: AdminService = Provide[Container.admin_service]):
    all_professors = admin_service.get_all_professors(g.user)
    return render_template("admin.html", professors=all_professors)


@admin.delete("/<int:user_id>")
@inject
@login_required()
def delete_professor(user_id: int, admin_service: AdminService = Provide[Container.admin_service]):
    admin_service.delete_professor(g.user, user_id)
    response = Response("Deleted professor")
    response.headers["HX-Location"] = url_for('admin.get_professors')
    return response


@admin.patch("/<int:user_id>")
@inject
@login_required()
def update_professor(user_id: int, admin_service: AdminService = Provide[Container.admin_service]):
    body = request.form
    email = body["email"]
    name = body["name"]
    user_dto = UserDto.factory(user_id, name, email)
    admin_service.update_professor(g.user, user_dto)
    response = Response("Updated professor")
    response.headers["HX-Location"] = url_for('admin.get_professors')
    return response
