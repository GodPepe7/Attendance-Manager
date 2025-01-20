class InvalidCredentialsException(Exception):
    def __init__(self):
        self.message = "Invalid Credentials."
        super().__init__(self.message)


class AttendanceLoggingException(Exception):
    pass


class InvalidInputException(Exception):
    pass


class NotFoundException(Exception):
    pass


class UnauthorizedException(Exception):
    pass


class QrCodeExpired(Exception):
    pass


class NoPasswordAndExpirationYetException(Exception):
    pass
