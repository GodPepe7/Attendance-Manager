import fernet
from dependency_injector import containers, providers

from src.adapters.primary.config.db import DB
from src.adapters.secondary.clock_impl import Clock
from src.adapters.secondary.course_repository_impl import CourseRepository
from src.adapters.secondary.course_student_repository_impl import CourseStudentRepository
from src.adapters.secondary.lecture_repository_impl import LectureRepository
from src.adapters.secondary.user_repository_impl import UserRepository
from src.application.primary_ports.attendance_service import AttendanceService
from src.application.primary_ports.course_service import CourseService
from src.application.encryptor import Encryptor
from src.application.primary_ports.lecture_service import LectureService
from src.application.primary_ports.user_service import UserService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.db_uri.from_env("DB_URI", default="sqlite:///test2.db")
    config.encryption_key.from_value(fernet.Fernet.generate_key())

    db = providers.Singleton(DB, db_uri=config.db_uri())
    db_session = providers.Factory(db.provided.get_db_session())

    clock = providers.Factory(
        Clock
    )

    course_repo = providers.Factory(
        CourseRepository,
        session=db_session
    )

    lecture_repo = providers.Factory(
        LectureRepository,
        session=db_session
    )

    user_repo = providers.Factory(
        UserRepository,
        session=db_session
    )

    course_student_repo = providers.Factory(
        CourseStudentRepository,
        session=db_session
    )

    encryption_service = providers.Factory(
        Encryptor,
        key=config.encryption_key()
    )

    attendance_service = providers.Factory(
        AttendanceService,
        course_student_repo=course_student_repo,
        lecture_repo=lecture_repo,
        course_repo=course_repo,
        encryptor=encryption_service,
        clock=clock
    )

    course_service = providers.Factory(
        CourseService,
        repo=course_repo,
    )

    lecture_service = providers.Factory(
        LectureService,
        repo=lecture_repo,
        course_repo=course_repo,
    )

    user_service = providers.Factory(
        UserService,
        repo=user_repo
    )
