from rest_framework import serializers
from .models import PasswordEntry


class PasswordEntrySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    decrypted_password = serializers.SerializerMethodField()

    class Meta:
        model = PasswordEntry
        fields = ['service_name', 'password', 'decrypted_password']

    def get_decrypted_password(self, obj):
        return obj.decrypt_password()

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['encrypted_password'] = PasswordEntry().encrypt_password(password)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.encrypted_password = PasswordEntry().encrypt_password(validated_data.pop('password'))
        return super().update(instance, validated_data)
