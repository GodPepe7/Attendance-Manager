import datetime
import random

import fernet

from src.application.primary_ports.encryption_service import EncryptionService


class TestEncryptionService:
    encryptor = EncryptionService(fernet.Fernet.generate_key())

    def test_encrypt_lecture_and_time_and_decrypt_back_gives_orginal_back(self):
        now = datetime.datetime.now().replace(microsecond=0)
        lecture_id = random.randint(1, 999999)
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")

        encrypted_lecture_and_time = self.encryptor.encrypt_lecture_and_time(lecture_id, now)
        decrypted_lecture_id, decrypted_expiration_time = self.encryptor.decrypt_to_lecture_and_time(
            encrypted_lecture_and_time)

        assert f"{lecture_id},{now_str}" != encrypted_lecture_and_time
        assert lecture_id == decrypted_lecture_id and now == decrypted_expiration_time
