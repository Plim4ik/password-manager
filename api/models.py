from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.conf import settings

class PasswordEntry(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь')
    )
    service_name = models.CharField(
        max_length=255,
        verbose_name=_('Имя сервиса')
    )
    encrypted_password = models.BinaryField(verbose_name=_('Зашифрованный пароль'))

    class Meta:
        unique_together = ('user', 'service_name')
        verbose_name = _('Пароль')
        verbose_name_plural = _('Пароли')

    def __str__(self):
        return f"{self.user.username} - {self.service_name}"
    
    def encrypt_password(self, password: str):
        if not settings.FERNET_KEY:
            raise ValueError("🔴 Ошибка: FERNET_KEY отсутствует в настройках!")
        fernet = Fernet(settings.FERNET_KEY.encode())
        return fernet.encrypt(password.encode())


    def decrypt_password(self):
        """Расшифровываем пароль при запросе из БД"""
        if not settings.FERNET_KEY:
            raise ValueError("🔴 Ошибка: FERNET_KEY отсутствует в настройках!")

        fernet = Fernet(settings.FERNET_KEY.encode())

        encrypted_password = bytes(self.encrypted_password)

        return fernet.decrypt(encrypted_password).decode()

    