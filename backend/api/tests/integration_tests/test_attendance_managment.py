# test_attendance_management.py
from django.test import TestCase
from rest_framework.test import APIClient
from api.models import CustomUser, Student, Class, Instructor, Attendance
from django.utils import timezone


class AttendanceManagementTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create admin user and authenticate
        self.admin = CustomUser.objects.create_user(
            email='admin@example.com',
            password='adminpass123',
            role='admin'
        )
        self.client.force_authenticate(user=self.admin)

        # Create instructor
        self.instructor = CustomUser.objects.create_user(
            email='instructor@example.com',
            password='instrpass123',
            role='instructor'
        )

        # Create student user
        self.student_user = CustomUser.objects.create_user(
            email='student@test.com',
            password='studpass123',
            role='student'
        )

        # Create test data
        self.student = Student.objects.create(
            user=self.student_user,
            first_name='Test',
            last_name='Student',
            email='student@test.com',
            phone_number='123456789',
            date_of_birth='2000-01-01'
        )

        self.instructor_profile = Instructor.objects.create(
            first_name='Test',
            last_name='Instructor',
            email='instructor@example.com',
            specialization='Salsa'
        )

        self.dance_class = Class.objects.create(
            name='Test Class',
            style='Salsa',
            max_participants=10,
            instructor=self.instructor_profile,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=1)
        )

    def test_attendance_management_flow(self):
        # 1. Create attendance record
        attendance_data = {
            'student': self.student.id,
            'status': 'present',
            'notes': 'Arrived on time'
        }
        response = self.client.post(f'/api/classes/{self.dance_class.id}/attendance/', attendance_data)
        self.assertEqual(response.status_code, 201)

        # 2. Get attendance list for class
        response = self.client.get(f'/api/classes/{self.dance_class.id}/attendance/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        # 3. Update attendance status
        update_data = {'status': 'late'}
        response = self.client.patch(
            f'/api/classes/{self.dance_class.id}/attendance/{self.student.id}/',
            update_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'late')

        # 4. Check attendance report
        response = self.client.get('/api/reports/attendance/month/')
        self.assertEqual(response.status_code, 200)