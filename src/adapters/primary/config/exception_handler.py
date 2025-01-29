from src.application.exceptions import InvalidInputException, InvalidCredentialsException, NotFoundException, \
    QrCodeExpired, \
    UnauthorizedException, NoPasswordAndExpirationYetException

EXCEPTION_DICT = {
    InvalidInputException: 400,
    InvalidCredentialsException: 403,
    UnauthorizedException: 403,
    QrCodeExpired: 403,
    NotFoundException: 404,
    NoPasswordAndExpirationYetException: 404
}
