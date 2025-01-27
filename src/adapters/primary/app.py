# fix windows registry stuff
import mimetypes

from werkzeug.middleware.proxy_fix import ProxyFix

from src.adapters.primary.blueprint.student_bp import student_bp

mimetypes.add_type('application/javascript', '.js')

import logging
import traceback

from flask import Flask, jsonify, redirect, url_for

from src.adapters.primary.blueprint import attendance, auth, course, lecture, user
from src.adapters.primary.blueprint.attendance import attendance as attendance_bp
from src.adapters.primary.blueprint.auth import auth as auth_bp
from src.adapters.primary.blueprint.course import course as course_bp
from src.adapters.primary.blueprint.lecture import lecture as lecture_bp
from src.adapters.primary.blueprint.user import user as user_bp
from src.adapters.primary.config.container import Container
from src.adapters.primary.config.exception_handler import EXCEPTION_DICT


def create_app() -> Flask:
    app = Flask(__name__, static_url_path='/static')
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    app.config.from_pyfile("config/config.py")
    container = Container()
    container.wire(modules=[attendance, auth, course, lecture, user])
    app.container = container
    db = Container.db()
    db.create_tables()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.get_db_session().remove()

    @app.errorhandler(Exception)
    def handle_exception(error):
        for exc_type, code in EXCEPTION_DICT.items():
            if isinstance(error, exc_type):
                return str(error), code

        response = {"error": "InternalServerError"}
        logging.error(error)
        logging.error("Traceback:\n%s", traceback.format_exc())
        return jsonify(response), 500

    app.register_blueprint(auth_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(lecture_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(student_bp)
    app.add_url_rule("/", "index", lambda: redirect(url_for("auth.login")))

    return app
