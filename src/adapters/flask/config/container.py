from os import environ

from dependency_injector import containers, providers

from src.adapters.flask.config.db import DB
from src.adapters.repositories.course_repository_impl import CourseRepository
from src.adapters.repositories.enrollment_repository_impl import EnrollmentRepository
from src.adapters.repositories.lecture_repository_impl import LectureRepository
from src.adapters.repositories.user_repository_impl import UserRepository
from src.domain.services.admin_service import AdminService
from src.domain.services.attendance_service import AttendanceService
from src.domain.services.course_service import CourseService
from src.domain.services.encryption_service import EncryptionService
from src.domain.services.lecture_service import LectureService
from src.domain.services.user_service import UserService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    db_uri = environ.get("DB_URI")
    db = providers.Singleton(DB, db_uri=environ.get("DB_URI"))
    db_session = providers.Factory(db.provided.get_db_session())

    course_repo = providers.Factory(
        CourseRepository,
        session=db_session
    )

    lecture_repo = providers.Factory(
        LectureRepository,
        session=db_session
    )

    user_repository = providers.Factory(
        UserRepository,
        session=db_session
    )

    enrollment_repository = providers.Factory(
        EnrollmentRepository,
        session=db_session
    )

    encryption_service = providers.Factory(
        EncryptionService,
        fernet_key=environ.get("ENCRYPTION_KEY").encode()
    )

    attendance_service = providers.Factory(
        AttendanceService,
        enrollment_repo=enrollment_repository,
        lecture_repo=lecture_repo,
        course_repo=course_repo,
        encryptor=encryption_service
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
        repo=user_repository
    )

    admin_service = providers.Factory(
        AdminService,
        user_repo=user_repository
    )
