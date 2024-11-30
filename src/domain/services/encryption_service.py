from datetime import datetime
from typing import Optional

from fernet import Fernet


class EncryptionService:
    def __init__(self, fernet_key: bytes):
        self.cipher_suite = Fernet(fernet_key)

    def encrypt_date(self, date_time: datetime) -> str:
        datetime_string = date_time.strftime("%Y-%m-%d %H:%M:%S")
        return self.cipher_suite.encrypt(datetime_string.encode()).decode()

    def decrypt_date(self, encrypted_str: str) -> Optional[datetime]:
        try:
            decrypted_str = self.cipher_suite.decrypt(encrypted_str.encode()).decode()
            date_time = datetime.strptime(decrypted_str, "%Y-%m-%d %H:%M:%S")
            return date_time
        except Exception:
            return None
