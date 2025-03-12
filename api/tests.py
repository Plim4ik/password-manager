from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.conf import settings
from api.models import PasswordEntry
from cryptography.fernet import Fernet
from django.urls import reverse
from django.db.utils import IntegrityError

class PasswordEntryTestCase(TestCase):
    def setUp(self):
        """Подготовка тестового окружения"""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.user2 = User.objects.create_user(username="otheruser", password="testpassword2")
        self.fernet = Fernet(settings.FERNET_KEY.encode())
        self.raw_password = "secure_password_123"
        self.encrypted_password = self.fernet.encrypt(self.raw_password.encode())

        self.entry = PasswordEntry.objects.create(
            user=self.user,
            service_name="GitHub",
            encrypted_password=self.encrypted_password
        )

    def test_password_encryption(self):
        """Проверяем, что шифрование пароля работает корректно"""
        new_password = "new_secure_password"
        encrypted = self.entry.encrypt_password(new_password)
        decrypted = self.fernet.decrypt(encrypted).decode()

        self.assertEqual(new_password, decrypted, "🔴 Ошибка: Пароль после расшифровки не совпадает!")

    def test_password_decryption(self):
        """Проверяем, что расшифровка пароля работает корректно"""
        decrypted_password = self.entry.decrypt_password()
        self.assertEqual(decrypted_password, self.raw_password, "🔴 Ошибка: Неверный пароль после расшифровки!")

    def test_password_storage(self):
        """Проверяем, что зашифрованный пароль корректно хранится в базе"""
        self.entry.refresh_from_db()
        self.assertEqual(bytes(self.entry.encrypted_password), self.encrypted_password, "🔴 Ошибка: Данные в БД повреждены!")

    def test_unique_constraint(self):
        """Проверяем, что нельзя создать дубликат пароля для одного сервиса"""
        with self.assertRaises(IntegrityError):
                    PasswordEntry.objects.create(user=self.user, service_name="GitHub", encrypted_password=self.encrypted_password)


    def test_create_entry_success(self):
        """Проверяем создание нового пароля"""
        new_entry = PasswordEntry.objects.create(
            user=self.user,
            service_name="Google",
            encrypted_password=self.fernet.encrypt("my_google_pass".encode())
        )
        self.assertIsNotNone(new_entry.id, "🔴 Ошибка: Объект не создался в БД!")

    def test_create_entry_failure_without_encryption(self):
        """Проверяем создание пароля без шифрования (должен быть бинарным)"""
        with self.assertRaises(Exception):
            PasswordEntry.objects.create(user=self.user, service_name="Facebook", encrypted_password="plaintext_password")

    def test_access_denied_for_unauthenticated_users(self):
        """Проверяем, что неавторизованный пользователь не может получить доступ"""
        response = self.client.get(reverse('password_entry_list'))
        self.assertEqual(response.status_code, 401, "🔴 Ошибка: Неавторизованный пользователь получил доступ!")


