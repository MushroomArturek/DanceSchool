# test_payment_management.py
from django.test import TestCase
from rest_framework.test import APIClient
from api.models import CustomUser, Student, Payment
from django.utils import timezone


class PaymentManagementTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = CustomUser.objects.create_user(
            email='admin@example.com',
            password='adminpass123',
            role='admin'
        )
        self.client.force_authenticate(user=self.admin)

        self.student_user = CustomUser.objects.create_user(
            email='student@test.com',
            password='studpass123',
            role='student'
        )
        self.student = Student.objects.create(
            user=self.student_user,
            first_name='Test',
            last_name='Student',
            email='student@test.com',
            phone_number='123456789',
            date_of_birth='2000-01-01'
        )

    def test_payment_management_flow(self):
        # 1. Create payment
        payment_data = {
            'student': self.student.id,
            'amount': '150.00',
            'payment_type': 'monthly',
            'payment_method': 'transfer'
        }
        response = self.client.post('/api/payments/create/', payment_data)
        self.assertEqual(response.status_code, 201)

        # 2. Get payment list
        response = self.client.get('/api/payments/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        # 3. Get payment details
        payment_id = response.data[0]['id']
        response = self.client.get(f'/api/payments/{payment_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['amount'], '150.00')

        # 4. Update payment
        update_data = {'payment_method': 'cash'}
        response = self.client.patch(f'/api/payments/{payment_id}/update/', update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['payment_method'], 'cash')