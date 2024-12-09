import datetime

import fernet

from src.domain.services.encryption_service import EncryptionService


class TestEncryptionService:
    encryptor = EncryptionService(fernet_key=fernet.Fernet.generate_key())

    def test_encrypt_and_decrypt_back(self):
        now = datetime.datetime.now().replace(microsecond=0)
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")

        encrypted = self.encryptor.encrypt_date(now)
        decrypted = self.encryptor.decrypt_date(encrypted)

        assert now != encrypted and now_str != encrypted
        assert now == decrypted
