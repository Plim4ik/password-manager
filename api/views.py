# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import PasswordEntry, MasterPassword
from .serializers import PasswordSerializer, MasterPasswordSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes


class PasswordViewSet(viewsets.GenericViewSet):
    serializer_class = PasswordSerializer

    def _get_master_password(self, user):
        """Получение мастер-пароля пользователя."""
        try:
            master_password_obj = MasterPassword.objects.get(user=user)
            return master_password_obj.get_master_password(master_password_obj.encryption_key)
        except MasterPassword.DoesNotExist:
            raise ValueError(_("Master password not set. Please set a master password first."))

    @extend_schema(
        parameters=[
            OpenApiParameter("service_name", OpenApiTypes.STR, OpenApiParameter.PATH, description="Name of the service"),
        ],
        request=PasswordSerializer,
        responses={201: PasswordSerializer, 400: dict, 403: dict},
        description="Create or update a password for a specific service."
    )
    @action(detail=False, methods=['post'], url_path='(?P<service_name>[^/.]+)')
    def create_or_update_password(self, request, service_name=None):
        """
        Создание или обновление пароля для сервиса.
        - Если сервис уже существует, пароль будет обновлен.
        - Если сервис не существует, он будет создан.
        """
        if not service_name:
            return Response({"error": _("service_name is required.")}, status=status.HTTP_400_BAD_REQUEST)

        password = request.data.get('password')
        if not password:
            return Response({"error": _("password is required.")}, status=status.HTTP_400_BAD_REQUEST)

        try:
            master_password = self._get_master_password(request.user)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        validated_data = {
            'service_name': service_name,
            'password': password
        }

        serializer = self.get_serializer(data=validated_data, context={'master_password': master_password})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter("service_name", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Part of the service name to search"),
        ],
        responses={200: PasswordSerializer(many=True), 403: dict},
        description="Search passwords by part of the service name."
    )
    @action(detail=False, methods=['get'], url_path='')
    def search_passwords(self, request):
        """Поиск паролей по части имени сервиса."""
        part_of_service_name = request.query_params.get('service_name', '')

        if not part_of_service_name:
            return Response({"error": _("service_name query parameter is required.")}, status=status.HTTP_400_BAD_REQUEST)

        try:
            master_password = self._get_master_password(request.user)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        entries = PasswordEntry.objects.filter(
            user=request.user,
            service_name__icontains=part_of_service_name
        )

        if not entries.exists():
            return Response({"message": _("No passwords found for the given service name.")}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(entries, many=True, context={'master_password': master_password})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=MasterPasswordSerializer,
        responses={201: MasterPasswordSerializer, 400: dict},
        description="Set or update the master password for the user."
    )
    @action(detail=False, methods=['post'], url_path='set-master-password')
    def set_master_password(self, request):
        """Установка или обновление мастер-пароля пользователя."""
        serializer = MasterPasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: dict, 403: dict},
        description="Get the current master password (only once)."
    )
    @action(detail=False, methods=['get'], url_path='get-master-password')
    def get_master_password(self, request):
        """Получение текущего мастер-пароля (только один раз)."""
        try:
            master_password_obj = MasterPassword.objects.get(user=request.user)
        except MasterPassword.DoesNotExist:
            return Response({"error": _("Master password is not set.")}, status=status.HTTP_403_FORBIDDEN)

        # Проверяем, что мастер-пароль можно получить только один раз
        if master_password_obj.is_revealed:
            return Response({"error": _("Master password has already been revealed.")}, status=status.HTTP_403_FORBIDDEN)

        master_password_obj.is_revealed = True
        master_password_obj.save()

        master_password = master_password_obj.get_master_password(master_password_obj.encryption_key)
        return Response({"master_password": master_password}, status=status.HTTP_200_OK)