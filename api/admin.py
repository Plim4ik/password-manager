from django.contrib import admin
from .models import PasswordEntry, MasterPassword

# Register your models here.
@admin.register(PasswordEntry)
class PasswordEntryAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'password']


@admin.register(MasterPassword)
class MasterPasswordAdmin(admin.ModelAdmin):
    list_display = ['user']