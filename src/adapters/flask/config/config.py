class BaseConfig:
    SECRET_KEY: str
    ENCRYPTION_KEY: bytes
    DEBUG: bool
    DATABASE_URI: str


class DevConfig(BaseConfig):
    SECRET_KEY = 'dev'
    ENCRYPTION_KEY = b'njox0E4EdV3zF3vP7E1LZ79tj9kM9BiX79W8pdfh7tg='
    DEBUG = True
    DATABASE_URI = 'sqlite:///dev.db'


class TestConfig(DevConfig):
    TESTING = True
    SECRET_KEY = 'test'
    DATABASE_URI = 'sqlite:///:memory'
