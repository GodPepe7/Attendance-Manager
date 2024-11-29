class InvalidCredentialsException(Exception):
    def __init__(self):
        self.message = "Invalid Credentials."
        super().__init__(self.message)


class InvalidInputException(Exception):
    pass


class NoCourseException(Exception):
    pass
