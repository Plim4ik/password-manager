import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

class PasswordEncryptor:
    def __init__(self):
        self.key = os.getenv("ENCRYPTION_KEY")
        if not self.key:
            self.key = Fernet.generate_key().decode()
            print(f"Generated new key: {self.key}")
        self.cipher = Fernet(self.key.encode())

    def encrypt(self, password):
        """Шифрование пароля."""
        return self.cipher.encrypt(password.encode()).decode()

    def decrypt(self, encrypted_password):
        """Расшифровка пароля."""
        return self.cipher.decrypt(encrypted_password.encode()).decode()
