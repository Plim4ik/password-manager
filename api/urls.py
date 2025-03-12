from django.urls import path, re_path
from .views import PasswordEntryViewSet

urlpatterns = [
    re_path(r'^password/search/$', PasswordEntryViewSet.as_view({'get': 'search'}), name='passwordentry-search'),
    path('password/<str:service_name>/', 
         PasswordEntryViewSet.as_view({'post': 'create', 'get': 'retrieve'}), 
         name='password_entry_detail'),
    path('password/', 
         PasswordEntryViewSet.as_view({'get': 'list'}), 
         name='password_entry_list'),

]