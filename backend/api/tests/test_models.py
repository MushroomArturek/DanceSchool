# backend/api/tests/test_models.py
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.test import TestCase
from api.models import CustomUser, Student, Class, Instructor, Booking, Payment, SchoolInfo, Attendance


class CustomUserTests(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_create_user(self):
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertTrue(user.check_password(self.user_data['password']))

    def test_user_str_method(self):
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data['email'])

    def test_create_user_without_email(self):
        invalid_data = self.user_data.copy()
        invalid_data.pop('email')
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(**invalid_data)

    def test_user_role_default(self):
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(user.role, 'student')


class StudentTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='student@example.com',
            password='testpass123',
            role='student'
        )
        self.student_data = {
            'user': self.user,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'student@example.com',
            'phone_number': '123456789',
            'date_of_birth': '2000-01-01'
        }

    def test_create_student(self):
        student = Student.objects.create(**self.student_data)
        self.assertEqual(student.first_name, self.student_data['first_name'])
        self.assertEqual(student.email, self.student_data['email'])

    def test_student_str_method(self):
        student = Student.objects.create(**self.student_data)
        expected = f"{self.student_data['first_name']} {self.student_data['last_name']}"
        self.assertEqual(str(student), expected)

    def test_unique_email(self):
        Student.objects.create(**self.student_data)
        duplicate_data = self.student_data.copy()
        duplicate_data['user'] = CustomUser.objects.create_user(
            email='other@example.com',
            password='testpass123'
        )

        # Create student instance without saving
        student = Student(**duplicate_data)

        # Try to validate - this should raise ValidationError
        with self.assertRaises(ValidationError):
            student.full_clean()


class ClassTests(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            specialization="Salsa"
        )

        self.class_data = {
            'name': 'Salsa Beginners',
            'style': 'Salsa',
            'max_participants': 10,
            'instructor': self.instructor,
            'start_time': timezone.now(),
            'end_time': timezone.now() + timedelta(hours=1),
            'days_of_week': 'MO,WE',
            'is_recurring': True,
            'room': 'Room 1'
        }

    def test_create_class(self):
        dance_class = Class.objects.create(**self.class_data)
        self.assertEqual(dance_class.name, self.class_data['name'])
        self.assertEqual(dance_class.style, self.class_data['style'])
        self.assertEqual(dance_class.instructor, self.instructor)

    def test_class_str_method(self):
        dance_class = Class.objects.create(**self.class_data)
        expected = f"Salsa Beginners (Salsa)"
        self.assertEqual(str(dance_class), expected)

    def test_available_slots(self):
        dance_class = Class.objects.create(**self.class_data)

        # Create a student and booking
        user = CustomUser.objects.create_user(
            email='student@example.com',
            password='testpass123'
        )
        student = Student.objects.create(
            user=user,
            first_name='John',
            last_name='Doe',
            email='student@example.com',
            phone_number='123456789',
            date_of_birth='2000-01-01'
        )

        # Check initial available slots
        self.assertEqual(dance_class.available_slots(), 10)

        # Create a booking
        Booking.objects.create(
            student=student,
            class_model=dance_class,
            status='confirmed'
        )

        # Check available slots after booking
        self.assertEqual(dance_class.available_slots(), 9)

    def test_max_participants_validation(self):
        invalid_data = self.class_data.copy()
        invalid_data['max_participants'] = -1

        dance_class = Class(**invalid_data)
        with self.assertRaises(ValidationError):
            dance_class.full_clean()


class PaymentTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='student@example.com',
            password='testpass123',
            role='student'
        )
        self.student = Student.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            email='student@example.com',
            phone_number='123456789',
            date_of_birth='2000-01-01'
        )
        self.payment_data = {
            'student': self.student,
            'amount': 100.00,
            'payment_type': 'single',
            'payment_method': 'cash',
            'status': 'pending',
            'created_at': timezone.now(),
            'paid_at': None,
            'valid_until': None
        }

    def test_create_payment(self):
        payment = Payment.objects.create(**self.payment_data)
        self.assertEqual(payment.amount, self.payment_data['amount'])
        self.assertEqual(payment.payment_type, self.payment_data['payment_type'])
        self.assertEqual(payment.payment_method, self.payment_data['payment_method'])
        self.assertEqual(payment.status, self.payment_data['status'])

    def test_payment_str_method(self):
        payment = Payment.objects.create(**self.payment_data)
        expected = f"{self.student} - {payment.amount} ({payment.status})"
        self.assertEqual(str(payment), expected)

    def test_payment_status_choices(self):
        payment = Payment.objects.create(**self.payment_data)
        self.assertIn(payment.status, dict(Payment.PAYMENT_STATUS).keys())

    def test_payment_type_choices(self):
        payment = Payment.objects.create(**self.payment_data)
        self.assertIn(payment.payment_type, dict(Payment.PAYMENT_TYPE).keys())

    def test_payment_method_choices(self):
        payment = Payment.objects.create(**self.payment_data)
        self.assertIn(payment.payment_method, dict(Payment.PAYMENT_METHOD).keys())


class BookingTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='student@example.com',
            password='testpass123',
            role='student'
        )
        self.student = Student.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            email='student@example.com',
            phone_number='123456789',
            date_of_birth='2000-01-01'
        )
        self.instructor = Instructor.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            specialization="Salsa"
        )
        self.class_instance = Class.objects.create(
            name='Salsa Beginners',
            style='Salsa',
            max_participants=10,
            instructor=self.instructor,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            days_of_week='MO,WE',
            is_recurring=True,
            room='Room 1'
        )
        self.booking_data = {
            'student': self.student,
            'class_model': self.class_instance,
            'status': 'confirmed'
        }

    def test_create_booking(self):
        booking = Booking.objects.create(**self.booking_data)
        self.assertEqual(booking.student, self.booking_data['student'])
        self.assertEqual(booking.class_model, self.booking_data['class_model'])
        self.assertEqual(booking.status, self.booking_data['status'])

    def test_booking_str_method(self):
        booking = Booking.objects.create(**self.booking_data)
        expected = f"{self.student} - {self.class_instance} ({self.booking_data['status']})"
        self.assertEqual(str(booking), expected)

    def test_unique_booking(self):
        Booking.objects.create(**self.booking_data)
        with self.assertRaises(ValidationError):
            duplicate_booking = Booking(**self.booking_data)
            duplicate_booking.full_clean()

    def test_booking_status_choices(self):
        booking = Booking.objects.create(**self.booking_data)
        self.assertIn(booking.status, dict(Booking._meta.get_field('status').choices).keys())


class InstructorTests(TestCase):
    def setUp(self):
        self.instructor_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com',
            'specialization': 'Salsa'
        }

    def test_create_instructor(self):
        instructor = Instructor.objects.create(**self.instructor_data)
        self.assertEqual(instructor.first_name, self.instructor_data['first_name'])
        self.assertEqual(instructor.last_name, self.instructor_data['last_name'])
        self.assertEqual(instructor.email, self.instructor_data['email'])
        self.assertEqual(instructor.specialization, self.instructor_data['specialization'])

    def test_instructor_str_method(self):
        instructor = Instructor.objects.create(**self.instructor_data)
        expected = f"{self.instructor_data['first_name']} {self.instructor_data['last_name']} - {self.instructor_data['specialization']}"
        self.assertEqual(str(instructor), expected)

    def test_unique_email(self):
        Instructor.objects.create(**self.instructor_data)
        duplicate_data = self.instructor_data.copy()  # Use same email
        with self.assertRaises(ValidationError):
            duplicate_instructor = Instructor(**duplicate_data)
            duplicate_instructor.full_clean()


class SchoolInfoTests(TestCase):
    def setUp(self):
        self.school_info_data = {
            'name': 'Dance Studio',
            'address': 'Street 123, City',
            'phone': '123456789',
            'email': 'contact@dancestudio.com',
            'bank_name': 'Test Bank',
            'bank_account': '1234567890',
            'bank_recipient': 'Dance Studio Ltd',
            'blik_number': '123456',
            'transfer_title_prefix': 'Payment - ',
            'tax_id': '1234567890'
        }

    def test_create_school_info(self):
        school_info = SchoolInfo.objects.create(**self.school_info_data)
        self.assertEqual(school_info.name, self.school_info_data['name'])
        self.assertEqual(school_info.email, self.school_info_data['email'])
        self.assertEqual(school_info.bank_account, self.school_info_data['bank_account'])
        self.assertEqual(school_info.blik_number, self.school_info_data['blik_number'])

    def test_school_info_str_method(self):
        school_info = SchoolInfo.objects.create(**self.school_info_data)
        self.assertEqual(str(school_info), self.school_info_data['name'])

    def test_optional_fields(self):
        data = self.school_info_data.copy()
        data.pop('blik_number')
        data.pop('tax_id')
        school_info = SchoolInfo.objects.create(**data)
        self.assertEqual(school_info.blik_number, '')
        self.assertEqual(school_info.tax_id, '')


class AttendanceTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='student@example.com',
            password='testpass123',
            role='student'
        )
        self.student = Student.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            email='student@example.com',
            phone_number='123456789',
            date_of_birth='2000-01-01'
        )
        self.instructor = Instructor.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            specialization="Salsa"
        )
        self.class_instance = Class.objects.create(
            name='Salsa Beginners',
            style='Salsa',
            max_participants=10,
            instructor=self.instructor,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            days_of_week='MO,WE',
            is_recurring=True,
            room='Room 1'
        )
        self.attendance_data = {
            'class_instance': self.class_instance,
            'student': self.student,
            'status': 'present',
            'is_booked': True,
            'notes': 'Test note'
        }

    def test_create_attendance(self):
        attendance = Attendance.objects.create(**self.attendance_data)
        self.assertEqual(attendance.class_instance, self.class_instance)
        self.assertEqual(attendance.student, self.student)
        self.assertEqual(attendance.status, self.attendance_data['status'])
        self.assertEqual(attendance.is_booked, self.attendance_data['is_booked'])
        self.assertEqual(attendance.notes, self.attendance_data['notes'])

    def test_attendance_status_choices(self):
        attendance = Attendance.objects.create(**self.attendance_data)
        valid_statuses = ['present', 'absent', 'late']
        self.assertIn(attendance.status, valid_statuses)

    def test_unique_class_student_combination(self):
        Attendance.objects.create(**self.attendance_data)
        with self.assertRaises(ValidationError):
            duplicate_attendance = Attendance(**self.attendance_data)
            duplicate_attendance.full_clean()

    def test_optional_notes_field(self):
        data = self.attendance_data.copy()
        data.pop('notes')
        attendance = Attendance.objects.create(**data)
        self.assertIsNone(attendance.notes)
