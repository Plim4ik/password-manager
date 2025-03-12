from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
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
    