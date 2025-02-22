# test_class_analytics.py
from django.test import TestCase
from rest_framework.test import APIClient
from api.models import CustomUser, Student, Class, Instructor, Booking
from django.utils import timezone


class ClassAnalyticsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = CustomUser.objects.create_user(
            email='admin@example.com',
            password='adminpass123',
            role='admin'
        )
        self.client.force_authenticate(user=self.admin)

        # Create test data
        self.instructor = Instructor.objects.create(
            first_name='Test',
            last_name='Instructor',
            email='instructor@test.com',
            specialization='Salsa'
        )

        # Create multiple classes and bookings for analytics
        styles = ['Salsa', 'Bachata', 'Kizomba']
        for style in styles:
            cls = Class.objects.create(
                name=f'{style} Class',
                style=style,
                max_participants=10,
                instructor=self.instructor,
                start_time=timezone.now(),
                end_time=timezone.now() + timezone.timedelta(hours=1)
            )

    def test_class_analytics_flow(self):
        # 1. Check monthly analytics
        response = self.client.get('/api/reports/analytics/month/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('popular_classes', response.data)
        self.assertIn('peak_hours', response.data)
        self.assertIn('style_distribution', response.data)

        # 2. Check quarterly analytics
        response = self.client.get('/api/reports/analytics/quarter/')
        self.assertEqual(response.status_code, 200)

        # 3. Verify style distribution
        self.assertEqual(len(response.data['style_distribution']), 3)