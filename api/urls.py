from django.urls import path
from .views import PasswordEntryViewSet

urlpatterns = [
    path('password/<str:service_name>/', PasswordEntryViewSet.as_view({'post': 'create', 'get': 'retrieve'})),
    path('password/', PasswordEntryViewSet.as_view({'get': 'list'})),
]
