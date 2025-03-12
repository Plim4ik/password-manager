# tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from .models import PasswordEntry

class PasswordManagerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_password(self):
        response = self.client.post('/password/yundex/', {'password': 'very_secret_pass'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PasswordEntry.objects.count(), 1)

    def test_retrieve_password(self):
        PasswordEntry.objects.create(service_name='yundex', encrypted_password='encrypted_password_here')
        response = self.client.get('/password/yundex/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['service_name'], 'yundex')

    def test_search_passwords(self):
        PasswordEntry.objects.create(service_name='yundex', encrypted_password='encrypted_password_here')
        response = self.client.get('/password/?service_name=yun')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)