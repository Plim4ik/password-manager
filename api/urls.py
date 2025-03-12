from django.urls import path
from .views import PasswordEntryViewSet

urlpatterns = [
    path('password/<str:service_name>/', 
         PasswordEntryViewSet.as_view({'post': 'create', 'get': 'retrieve'}), 
         name='password_entry_detail'),
    path('password/', 
         PasswordEntryViewSet.as_view({'get': 'list'}), 
         name='password_entry_list'),
]
