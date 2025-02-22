# test_serializers.py
from django.test import TestCase
from ..serializers import StudentSerializer
from ..models import Student, CustomUser, Class, Instructor

class StudentSerializerTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            role='student'
        )
        self.student_data = {
            'user': self.user,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'phone_number': '123456789',
            'date_of_birth': '2000-01-01'
        }

    def test_serializer_valid_data(self):
        serializer = StudentSerializer(data=self.student_data)
        self.assertTrue(serializer.is_valid())