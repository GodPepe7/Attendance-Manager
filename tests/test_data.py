import datetime

from werkzeug.security import generate_password_hash

from src.domain.entities.course import Course
from src.domain.entities.enrollment import Enrollment
from src.domain.entities.lecture import Lecture
from src.domain.entities.role import Role
from src.domain.entities.user import User

users = [
    User(name="alex", email="alex@abc.de", password_hash=generate_password_hash("1234"), role=Role.STUDENT, id=1),
    User(name="bob", email="bob@baumeister.de", password_hash=generate_password_hash("1234"), role=Role.PROFESSOR,
         id=2),
    User(name="unmei", email="unmei@gmail.com", password_hash=generate_password_hash("1234"), role=Role.STUDENT, id=3)
]

enrollments = [
    Enrollment(student=users[0], course_id=1, id=1),
    Enrollment(student=users[2], course_id=1, id=2),
    Enrollment(student=users[0], course_id=2, id=3)
]

lectures = [
    Lecture(
        id=1,
        course_id=1,
        date=datetime.date(2024, 12, 24),
        attended_students={enrollments[0], enrollments[1]},
    ),
    Lecture(
        id=2,
        course_id=1,
        date=datetime.date(2024, 12, 25),
        attended_students={enrollments[0]}
    ),
    Lecture(
        id=3,
        course_id=2,
        date=datetime.date(2024, 12, 31),
    ),
]

courses = [
    Course(
        id=1,
        name="Software Engineering",
        professor=users[1],
        enrolled_students={enrollments[0], enrollments[1]},
        lectures={lectures[0], lectures[1]}
    ),
    Course(
        id=2,
        name="Projectmanagement",
        professor=users[1],
        enrolled_students={enrollments[2]},
        lectures={lectures[2]}
    )
]
