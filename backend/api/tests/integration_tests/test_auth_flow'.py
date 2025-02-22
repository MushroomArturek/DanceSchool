# test_auth_flow.py
from django.test import TestCase
from rest_framework.test import APIClient
from api.models import CustomUser, Student


class AuthenticationFlowTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Simplified registration data matching the expected format
        self.register_data = {
            'email': 'new@example.com',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'student',
            'phone_number': '987654321',
            'date_of_birth': '2000-01-01'
        }

    def test_complete_auth_flow(self):
        # 1. Register new user
        response = self.client.post('/api/auth/register/', self.register_data, format='json')
        self.assertEqual(response.status_code, 201)

        # 2. Login with new user
        response = self.client.post('/api/auth/login/', {
            'email': 'new@example.com',
            'password': 'newpass123'
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

        # 3. Access protected endpoint with token
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/student/profile/')
        self.assertEqual(response.status_code, 200)

        # 4. Update profile
        response = self.client.patch('/api/student/profile/update/', {
            'phone_number': '111222333'
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Student.objects.get(user__email='new@example.com').phone_number,
            '111222333'
        )