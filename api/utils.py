# utils.py
from cryptography.fernet import Fernet

class PasswordEncryptor:
    def __init__(self, master_password):
        self.master_password = master_password.encode()
        self.cipher = Fernet(Fernet.generate_key())  # Генерация ключа на основе мастер-пароля

    def encrypt(self, password):
        """Шифрование пароля."""
        return self.cipher.encrypt(password.encode()).decode()

    def decrypt(self, encrypted_password):
        """Расшифровка пароля."""
        return self.cipher.decrypt(encrypted_password.encode()).decode()