# test_instructor_management.py
from django.test import TestCase
from rest_framework.test import APIClient
from api.models import CustomUser, Instructor
from django.utils import timezone


class InstructorManagementTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create admin user
        self.admin = CustomUser.objects.create_user(
            email='admin@example.com',
            password='adminpass123',
            role='admin'
        )
        self.client.force_authenticate(user=self.admin)

    def test_instructor_management_flow(self):
        # 1. Create new instructor
        instructor_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'specialization': 'Salsa'
        }
        response = self.client.post('/api/instructors/create/', instructor_data)
        self.assertEqual(response.status_code, 201)

        # Get instructor ID from created instructor
        created_instructor = Instructor.objects.get(email='john@example.com')
        instructor_id = created_instructor.id

        # 2. Get instructor details
        response = self.client.get(f'/api/instructors/{instructor_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'john@example.com')

        # 3. Update instructor
        update_data = {'specialization': 'Salsa, Bachata'}
        response = self.client.patch(f'/api/instructors/{instructor_id}/update/', update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['specialization'], 'Salsa, Bachata')

        # 4. Delete instructor
        response = self.client.delete(f'/api/instructors/{instructor_id}/delete/')
        self.assertEqual(response.status_code, 204)