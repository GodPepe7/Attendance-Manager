from datetime import datetime

from fernet import Fernet

from src.application.exceptions import InvalidInputException


class EncryptionService:
    def __init__(self, key: bytes):
        self.cipher_suite = Fernet(key)

    def encrypt_lecture_and_time(self, lecture_id: int, date_time: datetime) -> str:
        datetime_str = date_time.strftime("%Y-%m-%d %H:%M:%S")
        lecture_and_time_str = str(lecture_id) + "," + datetime_str
        return self.cipher_suite.encrypt(lecture_and_time_str.encode()).decode()

    def decrypt_to_lecture_and_time(self, encrypted_str: str) -> tuple[int, datetime]:
        try:
            lecture_and_time_str = self.cipher_suite.decrypt(encrypted_str.encode()).decode()
            lecture_and_time = lecture_and_time_str.split(",")
            lecture_id = int(lecture_and_time[0])
            date_time = datetime.strptime(lecture_and_time[1], "%Y-%m-%d %H:%M:%S")
            return lecture_id, date_time
        except Exception:
            raise InvalidInputException("Qr Code String is not valid")
