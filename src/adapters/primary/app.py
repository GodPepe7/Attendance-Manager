# fix windows registry stuff
import mimetypes

mimetypes.add_type('application/javascript', '.js')

from dependency_injector import containers
from werkzeug.middleware.proxy_fix import ProxyFix
from src.adapters.primary.config.container import Container
from src.adapters.primary.blueprint import attendance, auth, lecture, user, course
from src.adapters.primary.config.exception_handler import EXCEPTION_DICT
from src.adapters.primary.blueprint.attendance import attendance as attendance_bp
from src.adapters.primary.blueprint.auth import auth as auth_bp
from src.adapters.primary.blueprint.course import course as course_bp
from src.adapters.primary.blueprint.lecture import lecture as lecture_bp
from src.adapters.primary.blueprint.user import admin as user_bp
from src.adapters.primary.blueprint.student_bp import student_bp

import logging
import traceback

from flask import Flask, jsonify, redirect, url_for


class FlaskApp:
    def __init__(self, container: containers.DeclarativeContainer, custom_config: dict = None):
        self.container = container
        self.custom_config = custom_config
        self.app = self._create_app()

    def _create_app(self) -> Flask:
        app = Flask(__name__, static_url_path='/static')
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
        if self.custom_config:
            for key, val in self.custom_config.items():
                app.config[key] = val
        else:
            app.config.from_pyfile("config/config.py")

        app.config['APPLICATION_ROOT'] = '/'
        app.config['PREFERRED_URL_SCHEME'] = 'https'

        self.container.wire(modules=[attendance, auth, course, lecture, user])
        app.container = self.container

        db = self.container.db()
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

    def run(self, *args, **kwargs):
        self.app.run(*args, **kwargs)


def create_app():
    flaskApp = FlaskApp(Container())
    return flaskApp.app
