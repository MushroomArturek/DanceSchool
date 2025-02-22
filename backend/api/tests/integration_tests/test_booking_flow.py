# test_booking_flow.py
from django.test import TestCase
from rest_framework.test import APIClient
from api.models import CustomUser, Student, Class, Instructor, Booking
from django.utils import timezone


class BookingFlowTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test user and authenticate
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            role='student'
        )
        self.client.force_authenticate(user=self.user)

        # Create complete test data
        self.student = Student.objects.create(
            user=self.user,
            first_name='Test',
            last_name='Student',
            email='test@example.com',
            phone_number='123456789',
            date_of_birth='2000-01-01'
        )

        self.instructor = Instructor.objects.create(
            first_name='Test',
            last_name='Instructor',
            email='instructor@test.com',
            specialization='Salsa'
        )

        self.dance_class = Class.objects.create(
            name='Test Class',
            style='Salsa',
            max_participants=10,
            instructor=self.instructor,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=1)
        )

    def test_complete_booking_flow(self):
        # 1. Get available classes
        response = self.client.get('/api/classes/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        # 2. Get class details
        class_id = response.data[0]['id']
        response = self.client.get(f'/api/classes/{class_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Class')

        # 3. Create booking
        response = self.client.post('/api/bookings/create/', {
            'class_model': class_id,
            'status': 'confirmed'
        })
        self.assertEqual(response.status_code, 201)
        booking_id = response.data['id']

        # 4. Verify booking exists
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], booking_id)

        # 5. Cancel booking
        response = self.client.delete(f'/api/bookings/{booking_id}/delete/')
        self.assertEqual(response.status_code, 204)

        # 6. Verify booking is cancelled
        booking = Booking.objects.get(id=booking_id)
        self.assertEqual(booking.status, 'cancelled')