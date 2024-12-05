from src.domain.exceptions import InvalidInputException, InvalidCredentialsException, NotFoundException, QrCodeExpired, \
    UnauthorizedException

EXCEPTION_DICT = {
    InvalidInputException: 400,
    InvalidCredentialsException: 403,
    UnauthorizedException: 403,
    QrCodeExpired: 403,
    NotFoundException: 404,
}
