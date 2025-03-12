from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import PasswordEntry
from .serializers import PasswordEntrySerializer


class PasswordEntryViewSet(mixins.CreateModelMixin,  
                           mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """ViewSet для управления паролями (шифрованное хранилище)"""
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordEntrySerializer

    def get_queryset(self):
        """Фильтруем пароли только по пользователю"""
        search_query = self.request.GET.get("service_name", "")
        return PasswordEntry.objects.filter(user=self.request.user, service_name__icontains=search_query)

    def create(self, request, *args, **kwargs):
        """Создать или обновить пароль"""
        service_name = kwargs.get("service_name")
        password = request.data.get("password")

        if not password:
            return Response({"error": "Password is required"}, status=400)

        password_entry, created = PasswordEntry.objects.update_or_create(
            user=request.user,
            service_name=service_name,
            defaults={"encrypted_password": PasswordEntry().encrypt_password(password)}
        )

        serializer = self.get_serializer(password_entry)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Получить пароль по имени сервиса"""
        service_name = kwargs.get("service_name")
        password_entry = get_object_or_404(PasswordEntry, user=request.user, service_name=service_name)
        serializer = self.get_serializer(password_entry)
        return Response(serializer.data)
