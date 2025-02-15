from src.application.exceptions import InvalidInputException, InvalidCredentialsException, NotFoundException, \
    QrCodeExpired, UnauthorizedException, NoPasswordAndExpirationYetException, DuplicateException, \
    AttendanceLoggingException

EXCEPTION_DICT = {
    InvalidInputException: 400,
    DuplicateException: 400,
    QrCodeExpired: 400,
    AttendanceLoggingException: 400,
    InvalidCredentialsException: 403,
    UnauthorizedException: 403,
    NotFoundException: 404,
    NoPasswordAndExpirationYetException: 404
}
