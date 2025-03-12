from django.contrib import admin
from .models import PasswordEntry

# Register your models here.
@admin.register(PasswordEntry)
class PasswordEntryAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'encrypted_password']
