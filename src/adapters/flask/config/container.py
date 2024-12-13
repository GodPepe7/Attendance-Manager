from dependency_injector import containers, providers

from src.adapters.flask.config.sqlalchemy import get_db_session
from src.adapters.repositories.attendance_repository_impl import AttendanceRepository
from src.adapters.repositories.course_repository_impl import CourseRepository
from src.adapters.repositories.enrollment_repository_impl import EnrollmentRepository
from src.adapters.repositories.lecture_repository_impl import LectureRepository
from src.adapters.repositories.user_repository_impl import UserRepository
from src.domain.services.attendance_service import AttendanceService
from src.domain.services.authorizer_service import AuthorizerService
from src.domain.services.course_service import CourseService
from src.domain.services.encryption_service import EncryptionService
from src.domain.services.lecture_service import LectureService
from src.domain.services.user_service import UserService


class Container(containers.DeclarativeContainer):
    db_session = providers.Factory(get_db_session)
    config = providers.Configuration()

    attendance_repo = providers.Factory(
        AttendanceRepository,
        session=db_session
    )

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
        fernet_key=config.encryption_key
    )

    authorizer_service = providers.Factory(
        AuthorizerService,
        course_repo=course_repo,
        lecture_repo=lecture_repo
    )

    attendance_service = providers.Factory(
        AttendanceService,
        attendance_repo=attendance_repo,
        enrollment_repo=enrollment_repository,
        authorizer=authorizer_service,
        encryptor=encryption_service
    )

    course_service = providers.Factory(
        CourseService,
        repo=course_repo,
        authorizer=authorizer_service
    )

    lecture_service = providers.Factory(
        LectureService,
        repo=lecture_repo,
        authorizer=authorizer_service
    )

    user_service = providers.Factory(
        UserService,
        repo=user_repository
    )
