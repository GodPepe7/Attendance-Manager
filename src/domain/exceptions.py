class InvalidCredentialsException(Exception):
    """Invalid Credentials."""


class InvalidCoursePassword(Exception):
    """Wrong password"""


class InvalidInputException(Exception):
    pass


class NotFoundException(Exception):
    pass


class UnauthorizedException(Exception):
    pass


class QrCodeExpired(Exception):
    pass
