from datetime import datetime

from werkzeug.security import generate_password_hash

from src.application.entities.course import Course
from src.application.entities.course_student import CourseStudent
from src.application.entities.lecture import Lecture
from src.application.entities.role import Role
from src.application.entities.user import User

_user_password_hash = generate_password_hash("test")

users = [
    User("chad", "prof@htw.de", _user_password_hash, Role.PROFESSOR, 1),
    User("alex", "student@htw.de", _user_password_hash, Role.STUDENT, 2),
    User("ainz", "student2@htw.de", _user_password_hash, Role.STUDENT, 3),
    User("isagi", "student3@htw.de", _user_password_hash, Role.STUDENT, 4),
    User("luffy", "student4@htw.de", _user_password_hash, Role.STUDENT, 5),
    User("admin", "admin@htw.de", _user_password_hash, Role.ADMIN, 6),
    User("dude", "prof2@htw.de", _user_password_hash, Role.PROFESSOR, 7),
]

lectures = [
    Lecture(1, datetime(2025, 1, 1), 1),
    Lecture(1, datetime(2025, 1, 2), 2),
    Lecture(1, datetime(2025, 1, 3), 3),
    Lecture(1, datetime(2025, 1, 23), 4),
    Lecture(2, datetime(2025, 1, 23), 5),
]

course_students = [
    CourseStudent(users[1], 1, {lectures[0]}, 1),
    CourseStudent(users[2], 1, {lectures[0], lectures[2], lectures[3]}, 2),
    CourseStudent(users[3], 1, {lectures[2]}, 3),
    CourseStudent(users[4], 1, {lectures[0], lectures[2], lectures[3]}, 4),
    CourseStudent(users[1], 2, {lectures[4]}, 5),
]

_course_password_hash = generate_password_hash("password")
course_expiration_datetime = datetime(2025, 1, 23, 12, 0)

courses = [
    Course("Softwareengineering", users[0], 1, _course_password_hash, course_expiration_datetime,
           {lectures[0], lectures[1], lectures[2], lectures[3]},
           {course_students[0], course_students[1], course_students[2], course_students[3]}),
    Course("Projectmanagement", users[0], 2, "", None, {lectures[4]}, {course_students[4]}),
    Course("Rizz 101", users[6], 3),
]
