from src.domain.exceptions import InvalidInputException, InvalidCredentialsException, NoCourseException

EXCEPTION_DICT = {
    InvalidInputException: 400,
    InvalidCredentialsException: 403,
    NoCourseException: 404
}
