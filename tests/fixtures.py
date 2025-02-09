import pytest

from src.adapters.primary.config.db import DB
from tests.test_data import courses


@pytest.fixture
def db_session():
    db = DB("sqlite:///:memory:")
    db.create_tables()
    session = db.get_db_session()
    session.add_all(courses)
    session.expunge_all()
    yield session
    session.close()
