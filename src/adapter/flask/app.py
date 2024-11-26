from flask import Flask

from src.adapter.flask.blueprint.auth import auth_bp
from src.adapter.flask.blueprint.course import course_bp
from src.adapter.flask.config.sqlalchemy import db_session, init_db


def create_app() -> Flask:
    # container = Container()
    app = Flask(__name__)
    app.secret_key = "dev"
    # app.container = container
    with app.app_context():
        init_db()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    app.register_blueprint(auth_bp)
    app.register_blueprint(course_bp)
    app.add_url_rule("/", endpoint="index")
    return app