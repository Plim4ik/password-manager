# Generated by Django 5.1.7 on 2025-03-12 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_masterpassword_is_revealed'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MasterPassword',
        ),
    ]
