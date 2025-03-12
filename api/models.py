from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from cryptography.fernet import Fernet

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
    password = models.CharField(
        max_length=255,
        verbose_name=_('Пароль')
    )

    class Meta:
        unique_together = ('user', 'service_name')
        verbose_name = _('Пароль')
        verbose_name_plural = _('Пароли')

    def __str__(self):
        return f"{self.user.username} - {self.service_name}"
    

# models.py
from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import os

class MasterPassword(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь')
    )
    encrypted_master_password = models.CharField(
        max_length=255,
        verbose_name=_('Зашифрованный мастер-пароль')
    )
    encryption_key = models.CharField(
        max_length=255,
        verbose_name=_('Ключ шифрования для мастер-пароля')
    )
    is_revealed = models.BooleanField(default=False, verbose_name=_('Был ли мастер-пароль раскрыт'))

    class Meta:
        verbose_name = _('Мастер-пароль')
        verbose_name_plural = _('Мастер-пароли')

    def set_master_password(self, raw_password):
        """Установка мастер-пароля."""
        encryption_key = Fernet.generate_key().decode()
        fernet = Fernet(encryption_key)
        encrypted_password = fernet.encrypt(raw_password.encode()).decode()

        self.encrypted_master_password = encrypted_password
        self.encryption_key = encryption_key
        self.save()

    def get_master_password(self, raw_encryption_key):
        """Получение мастер-пароля."""
        if not self.encrypted_master_password or not self.encryption_key:
            return None

        fernet = Fernet(raw_encryption_key.encode())
        return fernet.decrypt(self.encrypted_master_password.encode()).decode()