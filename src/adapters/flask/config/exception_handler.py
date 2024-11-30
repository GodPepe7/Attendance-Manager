from src.domain.exceptions import InvalidInputException, InvalidCredentialsException, NotFoundException, QrCodeExpired

EXCEPTION_DICT = {
    InvalidInputException: 400,
    InvalidCredentialsException: 403,
    QrCodeExpired: 403,
    NotFoundException: 404,
}
