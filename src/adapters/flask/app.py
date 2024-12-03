import logging
import traceback

from flask import Flask, jsonify

from src.adapters.flask.blueprint.attendance import attendance
from src.adapters.flask.blueprint.auth import auth
from src.adapters.flask.blueprint.course import course
from src.adapters.flask.blueprint.lecture import lecture
from src.adapters.flask.config.exception_handler import EXCEPTION_DICT
from src.adapters.flask.config.sqlalchemy import db_session, init_db


def create_app() -> Flask:
    # container = Container()
    app = Flask(__name__)
    app.secret_key = "dev"
    # app.config["encryption_key"] = b'njox0E4EdV3zF3vP7E1LZ79tj9kM9BiX79W8pdfh7tg='
    # app.container = container
    with app.app_context():
        init_db()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

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

    app.register_blueprint(auth)
    app.register_blueprint(course)
    app.register_blueprint(lecture)
    app.register_blueprint(attendance)
    # app.add_url_rule("/", endpoint="index")

    return app
