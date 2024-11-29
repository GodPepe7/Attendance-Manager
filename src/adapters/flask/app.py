from flask import Flask, jsonify

from src.adapters.flask.blueprint.auth import auth_bp
from src.adapters.flask.blueprint.course import course_bp
from src.adapters.flask.config.sqlalchemy import db_session, init_db
from src.adapters.flask.exception_handler import EXCEPTION_DICT


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

    @app.errorhandler(Exception)
    def handle_exception(error):
        for exc_type, code in EXCEPTION_DICT.items():
            if isinstance(error, exc_type):
                response = {"error": exc_type.__name__, "message": str(error)}
                return jsonify(response), code

        response = {"error": "InternalServerError", "message": str(error)}
        return jsonify(response), 500

    app.register_blueprint(auth_bp)
    app.register_blueprint(course_bp)
    app.add_url_rule("/", endpoint="index")
    return app
