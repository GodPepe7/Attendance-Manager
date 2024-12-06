import logging
import traceback

from flask import Flask, jsonify, redirect, url_for

from src.adapters.flask.blueprint import attendance, auth, course, lecture
from src.adapters.flask.blueprint.attendance import attendance as attendance_bp
from src.adapters.flask.blueprint.auth import auth as auth_bp
from src.adapters.flask.blueprint.course import course as course_bp
from src.adapters.flask.blueprint.lecture import lecture as lecture_bp
from src.adapters.flask.config.config import DevConfig, TestConfig
from src.adapters.flask.config.container import Container
from src.adapters.flask.config.exception_handler import EXCEPTION_DICT
from src.adapters.flask.config.sqlalchemy import init_db

environments = {
    "dev": DevConfig(),
    "test": TestConfig()
}


def create_app(environment: str = "dev") -> Flask:
    app = Flask(__name__)
    app.config.from_object(environments.get(environment))

    with app.app_context():
        init_db(app.config.get("DATABASE_URI"))

        container = Container()
        container.wire(modules=[attendance, auth, course, lecture])
        container.config.encryption_key.from_value(app.config.get("ENCRYPTION_KEY"))
        app.container = container

    @app.errorhandler(Exception)
    def handle_exception(error):
        for exc_type, code in EXCEPTION_DICT.items():
            if isinstance(error, exc_type):
                response = {"error": exc_type.__name__, "message": str(error)}
                return jsonify(response), code

        response = {"error": "InternalServerError"}
        logging.error(error)
        logging.error("Traceback:\n%s", traceback.format_exc())
        return jsonify(response), 500

    app.register_blueprint(auth_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(lecture_bp)
    app.register_blueprint(attendance_bp)
    app.add_url_rule("/", "index", lambda: redirect(url_for("course.index")))

    return app
