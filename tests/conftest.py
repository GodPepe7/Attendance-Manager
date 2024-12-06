import datetime

import pytest
from werkzeug.security import generate_password_hash

from src.adapters.flask.config.sqlalchemy import init_db, get_db_session
from src.domain.entities.course import Course
from src.domain.entities.lecture import Lecture
from src.domain.entities.role import Role
from src.domain.entities.user import User


@pytest.fixture(scope="module")
def setup_database():
    init_db("sqlite:///:memory:")
    session = get_db_session()
    yield session
    session.close()


@pytest.fixture
def add_users(setup_database):
    session = setup_database
    users = [
        User("alex", "alex@abc.de", generate_password_hash("1234"), Role.STUDENT, 1),
        User("bob", "bob@baumeister.de", generate_password_hash("1234"), Role.PROFESSOR, 2),
        User("unmei", "unmei@gmail.com", generate_password_hash("1234"), Role.STUDENT, 3)
    ]
    session.add_all(users)
    session.commit()
    yield session, users
    session.query(User).delete()
    session.commit()


@pytest.fixture
def add_courses(add_users):
    session, users = add_users
    courses = [
        Course(name="Software Engineering", professor=users[1], id=1, enrolled_students={users[0], users[2]}),
        Course(name="Projectmanagement", professor=users[1], id=2, enrolled_students={users[0]}),
    ]
    session.add_all(courses)
    session.commit()
    yield session, courses
    session.query(Course).delete()
    session.commit()


@pytest.fixture
def add_lectures(add_courses):
    session, courses = add_courses
    software_engineering_students = list(courses[0].enrolled_students)
    project_management_students = list(courses[1].enrolled_students)
    lectures = [
        Lecture(
            id=1,
            course_id=courses[0].id,
            date=datetime.date(2024, 12, 10),
            attended_students=courses[0].enrolled_students
        ),
        Lecture(
            id=2,
            course_id=courses[0].id,
            date=datetime.date(2024, 12, 17),
            attended_students={software_engineering_students[1]}
        ),
        Lecture(
            id=3,
            course_id=courses[1].id,
            date=datetime.date(2024, 12, 12),
            attended_students={project_management_students[0]}
        ),
        Lecture(
            id=4,
            course_id=courses[1].id,
            date=datetime.date(2024, 12, 19)
        ),
    ]
    session.add_all(lectures)
    session.commit()
    yield session, courses
    session.query(Lecture).delete()
    session.commit()
