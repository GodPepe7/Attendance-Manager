from datetime import datetime
from threading import Thread

import pytest
from dependency_injector import providers
from sqlalchemy.orm import Session

from src.adapters.primary.app import FlaskApp
from src.adapters.primary.config.container import Container
from src.adapters.primary.config.tables import metadata
from src.application.secondary_ports.clock import IClock
from tests.test_data_e2e import courses, users


class FixedClock(IClock):
    def __init__(self, fixed_datetime: datetime):
        self.current = fixed_datetime

    def get_current_datetime(self) -> datetime:
        return self.current


@pytest.fixture(scope="module")
def storage(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("session")
    return tmp_path / "state.json"


@pytest.fixture(scope="session")
def start_test_app():
    flask_app: FlaskApp
    config_dict = {
        "DEBUG": False,
        "SECRET_KEY": "super_secret_key"
    }

    container = Container()
    flask_app = FlaskApp(container, config_dict)

    def run_app():
        flask_app.run(host="127.0.0.1", port=5001)

    thread = Thread(target=run_app, daemon=True)
    thread.start()

    return flask_app


@pytest.fixture(scope="session")
def add_test_data(start_test_app):
    flask_app = start_test_app
    db = flask_app.app.container.db()
    session = db.get_db_session()
    session.add_all(users)
    session.add_all(courses)
    session.commit()
    session.expunge_all()

    yield flask_app

    metadata.drop_all(bind=db.engine)


@pytest.fixture
def transactional_app(add_test_data):
    flask_app = add_test_data
    container = flask_app.container

    engine = container.db().engine
    connection = engine.connect()
    transaction = connection.begin()
    session = providers.ThreadSafeSingleton(Session, bind=connection)
    container.db_session.override(session)

    yield flask_app

    container.db_session().close()
    transaction.rollback()
    connection.close()
