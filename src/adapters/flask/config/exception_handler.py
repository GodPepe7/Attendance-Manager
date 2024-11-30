from src.domain.exceptions import InvalidInputException, InvalidCredentialsException, NotFoundException

EXCEPTION_DICT = {
    InvalidInputException: 400,
    InvalidCredentialsException: 403,
    NotFoundException: 404,
}
