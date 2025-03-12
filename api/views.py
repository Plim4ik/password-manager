from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
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
        """Фильтруем пароли только по пользователю и по имени сервиса, если указано"""
        search_query = self.request.GET.get("service_name", "")
        if search_query:
            return PasswordEntry.objects.filter(user=self.request.user, service_name__icontains=search_query)
        return PasswordEntry.objects.filter(user=self.request.user)

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

    @extend_schema(
        parameters=[
            OpenApiParameter("service_name", str, OpenApiParameter.QUERY, description="Часть имени сервиса для поиска")
        ]
    )
    def search(self, request, *args, **kwargs):
        """Поиск паролей по части имени сервиса"""
        search_query = request.GET.get("service_name", "")
        
        if not search_query:
            return Response({"detail": "service_name parameter is required for search."}, status=400)

        # Выводим поисковый запрос для отладки
        print(f"Search query: {search_query}")

        password_entries = PasswordEntry.objects.filter(
            user=request.user,
            service_name__icontains=search_query
        )
        
        # Выводим количество найденных записей для отладки
        print(f"Found {password_entries.count()} entries.")

        if not password_entries.exists():
            return Response({"detail": "No PasswordEntry matches the given query."}, status=404)

        serializer = self.get_serializer(password_entries, many=True)
        return Response(serializer.data)


    def permission_denied(self, request, message=None, code=None):
        """Возвращает кастомный ответ для неавторизованных пользователей"""
        if not request.user or request.user.is_anonymous:
            raise NotAuthenticated(detail="You are not authorized! Please log in.")
        super().permission_denied(request, message, code)
