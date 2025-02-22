# test_class_management.py
from django.test import TestCase
from rest_framework.test import APIClient
from api.models import CustomUser, Instructor, Class
from django.utils import timezone


class ClassManagementTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create admin user
        self.admin = CustomUser.objects.create_user(
            email='admin@example.com',
            password='adminpass123',
            role='admin'
        )
        self.client.force_authenticate(user=self.admin)

        # Create instructor
        self.instructor = Instructor.objects.create(
            first_name='Test',
            last_name='Instructor',
            email='instructor@test.com',
            specialization='Salsa'
        )

    def test_class_management_flow(self):
        # 1. Create new class
        class_data = {
            'name': 'Salsa Beginners',
            'style': 'Salsa',
            'max_participants': 12,
            'instructor': self.instructor.id,
            'start_time': timezone.now().isoformat(),
            'end_time': (timezone.now() + timezone.timedelta(hours=1)).isoformat(),
            'room': 'Room 1'
        }
        response = self.client.post('/api/classes/create/', class_data)
        self.assertEqual(response.status_code, 201)

        # Get created class by name
        created_class = Class.objects.get(name='Salsa Beginners')
        class_id = created_class.id

        # 2. Get class details
        response = self.client.get(f'/api/classes/{class_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Salsa Beginners')

        # 3. Update class
        update_data = {'max_participants': 15}
        response = self.client.patch(f'/api/classes/{class_id}/update/', update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['max_participants'], 15)

        # 4. Delete class
        response = self.client.delete(f'/api/classes/{class_id}/delete/')
        self.assertEqual(response.status_code, 204)