from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import CustomUser, Student, Instructor, Class, Booking, Payment, SchoolInfo, Attendance
from django.utils import timezone
from datetime import timedelta


class CustomTokenObtainPairViewTests(APITestCase):
    def setUp(self):
        self.login_url = reverse('token_obtain_pair')
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            role='student'
        )

    def test_obtain_token_success(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['firstName'], self.user.first_name)
        self.assertEqual(response.data['lastName'], self.user.last_name)
        self.assertEqual(response.data['role'], self.user.role)

    def test_obtain_token_invalid_credentials(self):
        data = {
            'email': 'test@example.com',
            'password': 'wrongpass'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_obtain_token_missing_fields(self):
        data = {'email': 'test@example.com'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RegisterUserViewTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.valid_data = {
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'phone_number': '123456789',
            'date_of_birth': '2000-01-01'
        }

    def test_register_user_success(self):
        response = self.client.post('/api/auth/register/', self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['email'], self.valid_data['email'])
        self.assertEqual(response.data['student']['first_name'], self.valid_data['first_name'])
        self.assertEqual(response.data['student']['last_name'], self.valid_data['last_name'])
        self.assertEqual(response.data['student']['email'], self.valid_data['email'])
        self.assertEqual(response.data['student']['phone_number'], self.valid_data['phone_number'])
        self.assertEqual(response.data['student']['date_of_birth'].strftime('%Y-%m-%d'),
                         self.valid_data['date_of_birth'])
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(Student.objects.count(), 1)

    def test_register_user_missing_required_fields(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop('email')
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertEqual(Student.objects.count(), 0)

    def test_register_user_invalid_email(self):
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'invalid-email'
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertEqual(Student.objects.count(), 0)

    def test_register_user_duplicate_email(self):
        # Create first user
        self.client.post(self.register_url, self.valid_data)

        # Try to create second user with same email
        response = self.client.post(self.register_url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(Student.objects.count(), 1)


class StudentViewTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            role='student'
        )
        self.student = Student.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            email='test@example.com',
            phone_number='123456789',
            date_of_birth='2000-01-01'
        )
        self.client.force_authenticate(user=self.user)

    def test_student_list(self):
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], self.student.first_name)

    def test_student_detail(self):
        response = self.client.get(f'/api/students/{self.student.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.student.email)

    def test_student_detail_not_found(self):
        response = self.client.get('/api/students/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_student_update(self):
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'phone_number': '987654321',
            'date_of_birth': '1999-12-31'
        }
        response = self.client.put(f'/api/students/{self.student.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertEqual(self.student.first_name, 'Jane')
        self.assertEqual(self.student.last_name, 'Smith')

    def test_student_update_unauthenticated(self):
        self.client.force_authenticate(user=None)
        data = {'first_name': 'Jane'}
        response = self.client.put(f'/api/students/{self.student.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_student_delete(self):
        response = self.client.delete(f'/api/students/{self.student.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0)

    def test_student_delete_not_found(self):
        response = self.client.delete('/api/students/999/delete/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_student_create_new_user(self):
        new_user = CustomUser.objects.create_user(
            email='unique_student@example.com',
            password='testpass123',
            role='student'
        )
        student = Student.objects.create(
            user=new_user,
            first_name='New',
            last_name='Student',
            email='unique_student@example.com',
            phone_number='555123456',
            date_of_birth='2002-01-01'
        )
        self.assertIsNotNone(student.id)
        self.assertEqual(student.user, new_user)


class StudentProfileViewTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testprofile@example.com',
            password='testpass123',
            role='student'
        )
        self.student = Student.objects.create(
            user=self.user,
            first_name='Profile',
            last_name='Test',
            email='testprofile@example.com',
            phone_number='123456789',
            date_of_birth='2000-01-01'
        )
        self.client.force_authenticate(user=self.user)

    def test_student_profile_retrieve_success(self):
        url = '/api/student/profile/'  # Adjust as needed
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.student.email)

    def test_student_profile_retrieve_not_found(self):
        # Create a new user without a student
        new_user = CustomUser.objects.create_user(
            email='nostudent@example.com',
            password='noStudent123',
            role='student'
        )
        self.client.force_authenticate(user=new_user)
        url = '/api/student/profile/'  # Adjust as needed
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_student_profile_update_success(self):
        url = '/api/student/profile/update/'  # Adjust as needed
        data = {
            'first_name': 'Updated',
            'last_name': 'Student'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertEqual(self.student.first_name, 'Updated')
        self.assertEqual(self.student.last_name, 'Student')

    def test_student_profile_update_not_found(self):
        # Create a new user without a student
        new_user = CustomUser.objects.create_user(
            email='nostudentupdate@example.com',
            password='noStudentUpdate123',
            role='student'
        )
        self.client.force_authenticate(user=new_user)
        url = '/api/student/profile/update/'  # Adjust as needed
        response = self.client.put(url, {'first_name': 'WillFail'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class InstructorViewTests(APITestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(
            email='admin@example.com',
            password='adminpass123',
            role='admin'
        )
        self.client.force_authenticate(user=self.admin_user)
        self.instructor = Instructor.objects.create(
            first_name='Test',
            last_name='Instructor',
            email='test_instructor@example.com',
            specialization='Salsa'
        )
        self.list_url = '/api/instructors/'
        self.detail_url = f'/api/instructors/{self.instructor.id}/'
        self.update_url = f'/api/instructors/{self.instructor.id}/update/'
        self.delete_url = f'/api/instructors/{self.instructor.id}/delete/'

    def test_instructor_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_instructor_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.instructor.email)

    def test_instructor_create(self):
        data = {
            'first_name': 'New',
            'last_name': 'Instructor',
            'email': 'new_instructor@example.com',
            'specialization': 'Bachata'
        }
        create_url = '/api/instructors/create/'
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_instructor_update(self):
        data = {'specialization': 'Updated Style'}
        response = self.client.patch(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_instructor_delete(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Instructor.objects.filter(id=self.instructor.id).exists())


class ClassViewTests(APITestCase):
    def setUp(self):
        # Create instructor for the classes
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            role='student'  # Make sure user has admin role
        )
        self.instructor = Instructor.objects.create(
            first_name='Test',
            last_name='Instructor',
            email='instructor@test.com',
            specialization='Test Style'
        )

        # Create test class
        self.test_class = Class.objects.create(
            name='Test Class',
            style='Test Style',
            max_participants=10,
            instructor=self.instructor
        )

        # Set up authentication
        self.client.force_authenticate(user=self.user)

    def test_retrieve_class(self):
        response = self.client.get(f'/api/classes/{self.test_class.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Class')

    def test_retrieve_nonexistent_class(self):
        response = self.client.get('/api/classes/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_class(self):
        data = {
            'name': 'New Class',
            'style': 'New Style',
            'max_participants': 15,
            'instructor': self.instructor.id
        }
        response = self.client.post('/api/classes/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Class.objects.count(), 2)

    def test_create_class_invalid_data(self):
        data = {
            'name': '',  # Invalid: empty name
            'style': 'New Style',
            'max_participants': 15,
            'instructor': self.instructor.id
        }
        response = self.client.post(f'/api/classes/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_class(self):
        data = {
            'name': 'Updated Class',
            'style': 'Updated Style',
            'max_participants': 20,
            'instructor': self.instructor.id
        }
        response = self.client.put(f'/api/classes/{self.test_class.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_class.refresh_from_db()
        self.assertEqual(self.test_class.name, 'Updated Class')

    def test_update_nonexistent_class(self):
        data = {'name': 'Updated Class'}
        response = self.client.put(f'/api/classes/999/update/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_class(self):
        response = self.client.delete(f'/api/classes/{self.test_class.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Class.objects.count(), 0)

    def test_delete_nonexistent_class(self):
        response = self.client.delete(f'/api/classes/999/delete/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookingViewTests(APITestCase):
    def setUp(self):
        # Create user and student
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            role='student'
        )
        self.student = Student.objects.create(
            user=self.user,
            first_name='Test',
            last_name='Student',
            email='test@example.com',
            phone_number='123456789',
            date_of_birth='2000-01-01'
        )

        # Create instructor
        self.instructor = Instructor.objects.create(
            first_name='Test',
            last_name='Instructor',
            email='instructor@test.com',
            specialization='Salsa'
        )

        # Create class
        self.dance_class = Class.objects.create(
            name='Test Class',
            style='Salsa',
            max_participants=2,
            instructor=self.instructor,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1)
        )

        # Create booking
        self.booking = Booking.objects.create(
            student=self.student,
            class_model=self.dance_class,
            status='confirmed'
        )

        self.client.force_authenticate(user=self.user)

    def test_booking_list(self):
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.booking.id)

    def test_booking_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_booking_create_success(self):
        new_class = Class.objects.create(
            name='Another Class',
            style='Bachata',
            max_participants=5,
            instructor=self.instructor,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1)
        )

        data = {
            'class_model': new_class.id,
            'status': 'confirmed'
        }
        response = self.client.post('/api/bookings/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)

    def test_booking_create_class_full(self):
        # Create another student and booking to fill the class
        another_user = CustomUser.objects.create_user(
            email='another@example.com',
            password='testpass123',
            role='student'
        )
        another_student = Student.objects.create(
            user=another_user,
            first_name='Another',
            last_name='Student',
            email='another@example.com',
            phone_number='987654321',
            date_of_birth='2000-01-01'
        )
        Booking.objects.create(
            student=another_student,
            class_model=self.dance_class,
            status='confirmed'
        )

        data = {
            'class_model': self.dance_class.id,
            'status': 'confirmed'
        }
        response = self.client.post('/api/bookings/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('No spots available', str(response.data))

    def test_booking_detail(self):
        response = self.client.get(f'/api/bookings/{self.booking.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.booking.id)

    def test_booking_detail_other_user(self):
        # Create another user and try to access first user's booking
        another_user = CustomUser.objects.create_user(
            email='another@example.com',
            password='testpass123',
            role='student'
        )
        self.client.force_authenticate(user=another_user)
        response = self.client.get(f'/api/bookings/{self.booking.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_booking_delete(self):
        response = self.client.delete(f'/api/bookings/{self.booking.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'cancelled')

    def test_booking_delete_other_user(self):
        another_user = CustomUser.objects.create_user(
            email='another@example.com',
            password='testpass123',
            role='student'
        )
        self.client.force_authenticate(user=another_user)
        response = self.client.delete(f'/api/bookings/{self.booking.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ReportViewTests(APITestCase):
    def setUp(self):
        # Create admin user
        self.admin_user = CustomUser.objects.create_user(
            email='admin@example.com',
            password='adminpass123',
            role='admin'
        )

        # Create instructor
        self.instructor = Instructor.objects.create(
            first_name='Test',
            last_name='Instructor',
            email='instructor@test.com',
            specialization='Salsa'
        )

        # Create student
        self.user = CustomUser.objects.create_user(
            email='student@example.com',
            password='testpass123',
            role='student'
        )
        self.student = Student.objects.create(
            user=self.user,
            first_name='Test',
            last_name='Student',
            email='student@example.com',
            phone_number='123456789',
            date_of_birth='2000-01-01'
        )

        # Create classes and bookings
        self.dance_class = Class.objects.create(
            name='Test Class',
            style='Salsa',
            max_participants=10,
            instructor=self.instructor,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1)
        )

        # Create booking
        self.booking = Booking.objects.create(
            student=self.student,
            class_model=self.dance_class,
            status='confirmed'
        )

    def test_attendance_report_unauthorized(self):
        url = reverse('attendance-report', kwargs={'period': 'month'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_attendance_report_forbidden(self):
        self.client.force_authenticate(user=self.user)  # Non-admin user
        url = reverse('attendance-report', kwargs={'period': 'month'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_attendance_report_success(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('attendance-report', kwargs={'period': 'month'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))
        if response.data:
            self.assertIn('class_name', response.data[0])
            self.assertIn('attendance_rate', response.data[0])
            self.assertIn('booked_slots', response.data[0])

    def test_attendance_report_different_periods(self):
        self.client.force_authenticate(user=self.admin_user)
        periods = ['week', 'month', 'quarter']

        for period in periods:
            url = reverse('attendance-report', kwargs={'period': period})
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_analytics_unauthorized(self):
        url = reverse('class-analytics', kwargs={'period': 'month'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_analytics_forbidden(self):
        self.client.force_authenticate(user=self.user)  # Non-admin user
        url = reverse('class-analytics', kwargs={'period': 'month'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_analytics_success(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('class-analytics', kwargs={'period': 'month'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('popular_classes', response.data)
        self.assertIn('peak_hours', response.data)
        self.assertIn('style_distribution', response.data)

    def test_analytics_different_periods(self):
        self.client.force_authenticate(user=self.admin_user)
        periods = ['month', 'quarter', 'year']

        for period in periods:
            url = reverse('class-analytics', kwargs={'period': period})
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_analytics_data_structure(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('class-analytics', kwargs={'period': 'month'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data['popular_classes'], list))
        self.assertTrue(isinstance(response.data['peak_hours'], list))
        self.assertTrue(isinstance(response.data['style_distribution'], list))

        if response.data['popular_classes']:
            class_data = response.data['popular_classes'][0]
            self.assertIn('name', class_data)
            self.assertIn('booking_count', class_data)

    def test_analytics_invalid_period(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('class-analytics', kwargs={'period': 'invalid'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Should default to month


class PaymentViewTests(APITestCase):
    def setUp(self):
        # Create user and student
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            role='student'
        )
        self.student = Student.objects.create(
            user=self.user,
            first_name='Test',
            last_name='Student',
            email='test@example.com',
            phone_number='123456789',
            date_of_birth='2000-01-01'
        )

        # Create test payment
        self.payment = Payment.objects.create(
            student=self.student,
            amount=100.00,
            payment_type='single',
            payment_method='cash',
            status='pending'
        )

        # Set up authentication
        self.client.force_authenticate(user=self.user)

    def test_payment_list(self):
        response = self.client.get('/api/payments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['amount'], '100.00')

    def test_payment_detail(self):
        response = self.client.get(f'/api/payments/{self.payment.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], '100.00')
        self.assertEqual(response.data['payment_type'], 'single')

    def test_payment_create(self):
        data = {
            'student': self.student.id,
            'amount': '50.00',
            'payment_type': 'single',
            'payment_method': 'transfer'
        }
        response = self.client.post('/api/payments/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 2)
        self.assertEqual(response.data['amount'], '50.00')

    def test_payment_update(self):
        data = {
            'student': self.student.id,
            'amount': '75.00',
            'payment_type': 'monthly',
            'payment_method': 'blik'
        }
        response = self.client.put(f'/api/payments/{self.payment.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.payment.refresh_from_db()
        self.assertEqual(str(self.payment.amount), '75.00')
        self.assertEqual(self.payment.payment_type, 'monthly')

    def test_payment_delete(self):
        response = self.client.delete(f'/api/payments/{self.payment.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Payment.objects.count(), 0)

    def test_payment_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/payments/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_payment_create_invalid_data(self):
        invalid_data = {
            'student': self.student.id,
            'amount': 'invalid',
            'payment_type': 'invalid_type'
        }
        response = self.client.post('/api/payments/create/', invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_payment_detail_nonexistent(self):
        response = self.client.get('/api/payments/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_payment_update_invalid_payment_type(self):
        data = {
            'student': self.student.id,
            'amount': '75.00',
            'payment_type': 'invalid_type',
            'payment_method': 'cash'
        }
        response = self.client.put(f'/api/payments/{self.payment.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class SchoolInfoViewTests(APITestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(
            email='admin@example.com',
            password='adminpass123',
            role='admin'
        )
        self.regular_user = CustomUser.objects.create_user(
            email='user@example.com',
            password='userpass123',
            role='student'
        )
        self.info_data = {
            'name': 'New Dance School',
            'address': 'New Street 123',
            'phone': '987654321',
            'email': 'new@school.com',
            'bank_name': 'New Bank',
            'bank_account': '11 1111 1111 1111 1111 1111 1111',
            'bank_recipient': 'New School Ltd',
            'transfer_title_prefix': 'New Payment - '
        }

    def test_get_school_info_no_existing_record(self):
        response = self.client.get('/api/school-info/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Szkoła Tańca')
        self.assertEqual(SchoolInfo.objects.count(), 1)

    def test_get_school_info_existing_record(self):
        school = SchoolInfo.objects.create(
            name='Test School',
            address='Test Address',
            phone='123456789',
            email='test@school.com'
        )
        response = self.client.get('/api/school-info/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test School')
        self.assertEqual(SchoolInfo.objects.count(), 1)

    def test_update_school_info_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put('/api/school-info/update/', self.info_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'New Dance School')
        self.assertEqual(response.data['email'], 'new@school.com')

    def test_update_school_info_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.put('/api/school-info/update/', self.info_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_school_info_unauthenticated(self):
        response = self.client.put('/api/school-info/update/', self.info_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AttendanceViewTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            role='student'
        )
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
            end_time=timezone.now() + timedelta(hours=1)
        )
        self.attendance = Attendance.objects.create(
            class_instance=self.dance_class,
            student=self.student,
            status='present',
            is_booked=True
        )
        self.client.force_authenticate(user=self.user)

    def test_get_attendance_list(self):
        response = self.client.get(f'/api/classes/{self.dance_class.id}/attendance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'present')

    def test_create_attendance(self):
        new_student = Student.objects.create(
            user=CustomUser.objects.create_user(
                email='new@example.com',
                password='pass123',
                role='student'
            ),
            first_name='New',
            last_name='Student',
            email='new@example.com',
            phone_number='987654321',
            date_of_birth='2000-01-01'
        )
        data = {
            'student': new_student.id,
            'status': 'present',
            'is_booked': True
        }
        response = self.client.post(
            f'/api/classes/{self.dance_class.id}/attendance/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendance.objects.count(), 2)

    def test_get_attendance_detail(self):
        response = self.client.get(
            f'/api/classes/{self.dance_class.id}/attendance/{self.student.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'present')

    def test_update_attendance(self):
        data = {'status': 'late'}
        response = self.client.patch(
            f'/api/classes/{self.dance_class.id}/attendance/{self.student.id}/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'late')

    def test_delete_attendance(self):
        response = self.client.delete(
            f'/api/classes/{self.dance_class.id}/attendance/{self.student.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Attendance.objects.count(), 0)

    def test_attendance_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(f'/api/classes/{self.dance_class.id}/attendance/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_attendance_nonexistent_class(self):
        response = self.client.get('/api/classes/995/attendance/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_attendance_nonexistent_student(self):
        response = self.client.get(
            f'/api/classes/{self.dance_class.id}/attendance/999/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
