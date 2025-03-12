# serializers.py
from .utils import PasswordEncryptor
from rest_framework import serializers
from .models import PasswordEntry, MasterPassword
from django.utils.translation import gettext_lazy as _

class PasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = PasswordEntry
        fields = ['service_name', 'password']

    def __init__(self, *args, **kwargs):
        self.master_password = kwargs.pop('master_password', None)
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        user = self.context['request'].user
        service_name = validated_data['service_name']
        raw_password = validated_data['password']

        if not self.master_password:
            raise serializers.ValidationError(_("Master password is required."))

        # Шифруем пароль
        encryptor = PasswordEncryptor(self.master_password)
        encrypted_password = encryptor.encrypt(raw_password)

        # Создаем запись
        entry, created = PasswordEntry.objects.update_or_create(
            user=user,
            service_name=service_name,
            defaults={'password': encrypted_password}
        )
        return entry

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if not self.master_password:
            data['password'] = None
        else:
            # Расшифруем пароль перед отправкой
            encryptor = PasswordEncryptor(self.master_password)
            data['password'] = encryptor.decrypt(instance.password)

        return data

class MasterPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterPassword
        fields = ['encrypted_master_password', 'encryption_key']

    def create(self, validated_data):
        user = self.context['request'].user
        raw_password = validated_data.get('raw_password')  # Передается из запроса

        # Создаем или обновляем мастер-пароль
        master_password, created = MasterPassword.objects.get_or_create(user=user)
        master_password.set_master_password(raw_password)
        return master_password