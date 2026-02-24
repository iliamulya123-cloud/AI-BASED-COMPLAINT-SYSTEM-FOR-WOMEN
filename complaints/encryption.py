from django.conf import settings
from cryptography.fernet import Fernet, InvalidToken


class EncryptionService:
    @staticmethod
    def _get_cipher():
        key = settings.ENCRYPTION_KEY
        if not key:
            return None
        return Fernet(key.encode())

    @classmethod
    def encrypt_text(cls, value: str) -> str:
        if not value:
            return value
        cipher = cls._get_cipher()
        if cipher is None:
            return value
        return cipher.encrypt(value.encode()).decode()

    @classmethod
    def decrypt_text(cls, value: str) -> str:
        if not value:
            return value
        cipher = cls._get_cipher()
        if cipher is None:
            return value
        try:
            return cipher.decrypt(value.encode()).decode()
        except InvalidToken:
            return value
