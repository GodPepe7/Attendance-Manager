from os import environ

SECRET_KEY = environ.get('SECRET_KEY')
ENCRYPTION_KEY = environ.get("ENCRYPTION_KEY").encode()
DEBUG = eval(environ.get("DEBUG"))
DATABASE_URI = environ.get("DATABASE_URI")
