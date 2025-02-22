# test_serializers.py
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from ..serializers import StudentSerializer, ClassDetailSerializer, ClassCreateSerializer, BookingSerializer, \
    RegisterUserSerializer, CustomTokenObtainPairSerializer, StudentUpdateSerializer, StudentCreateSerializer, \
    ClassUpdateSerializer, ClassCreateSerializer, InstructorSerializer, InstructorCreateSerializer, \
    InstructorUpdateSerializer, PaymentSerializer, SchoolInfoSerializer, AttendanceSerializer, \
    AttendanceReportSerializer, ClassAnalyticsSerializer
from ..models import Student, CustomUser, Class, Instructor, Booking, Attendance


class CustomTokenObtainPairSerializerTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            role='student'
        )

    def test_token_contains_role(self):
        token = CustomTokenObtainPairSerializer.get_token(self.user)
        self.assertEqual(token['role'], 'student')


class RegisterUserSerializerTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '123456789',
            'date_of_birth': '2000-01-01'
        }

    def test_serializer_with_valid_data(self):
        serializer = RegisterUserSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        # Check CustomUser creation
        self.assertEqual(user.email, self.valid_data['email'])
        self.assertEqual(user.role, 'student')

        # Check Student creation
        student = Student.objects.get(user=user)
        self.assertEqual(student.first_name, self.valid_data['first_name'])
        self.assertEqual(student.last_name, self.valid_data['last_name'])
        self.assertEqual(student.email, self.valid_data['email'])
        self.assertEqual(student.phone_number, self.valid_data['phone_number'])

    def test_serializer_missing_required_field(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop('first_name')
        serializer = RegisterUserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('first_name', serializer.errors)

    def test_serializer_invalid_email(self):
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'invalid-email'
        serializer = RegisterUserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_serializer_invalid_date_format(self):
        invalid_data = self.valid_data.copy()
        invalid_data['date_of_birth'] = 'invalid-date'
        serializer = RegisterUserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('date_of_birth', serializer.errors)


class StudentSerializerTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            role='student'
        )
        # Data for creating the model instance
        self.student_data = {
            'user': self.user,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'phone_number': '123456789',
            'date_of_birth': '2000-01-01'
        }

        # Create a different user for serializer testing
        self.user2 = CustomUser.objects.create_user(
            email='test2@example.com',
            password='testpass123',
            role='student'
        )
        # Data for testing the serializer with different email and user
        self.student_data_for_serializer = {
            'user': self.user2.id,
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'test2@example.com',
            'phone_number': '987654321',
            'date_of_birth': '2000-01-01'
        }
        self.student = Student.objects.create(**self.student_data)

    def test_serializer_contains_expected_fields(self):
        serializer = StudentSerializer(self.student)
        expected_fields = {
            'id', 'user', 'first_name', 'last_name',
            'email', 'phone_number', 'date_of_birth',
            'joined_date'
        }
        self.assertEqual(set(serializer.data.keys()), expected_fields)

    def test_serializer_valid_data(self):
        serializer = StudentSerializer(data=self.student_data_for_serializer)
        valid = serializer.is_valid()
        if not valid:
            print("Serializer Errors:", serializer.errors)  # Print detailed errors
            print("Data provided:", self.student_data_for_serializer)  # Print provided data
        self.assertTrue(valid)

    def test_serializer_invalid_email(self):
        invalid_data = self.student_data.copy()
        invalid_data['email'] = 'invalid-email'
        serializer = StudentSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())


class StudentUpdateSerializerTests(TestCase):
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
        self.valid_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'phone_number': '987654321',
            'date_of_birth': '1999-12-31'
        }

    def test_update_all_fields(self):
        serializer = StudentUpdateSerializer(self.student, data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        updated_student = serializer.save()

        self.assertEqual(updated_student.first_name, self.valid_data['first_name'])
        self.assertEqual(updated_student.last_name, self.valid_data['last_name'])
        self.assertEqual(updated_student.phone_number, self.valid_data['phone_number'])
        self.assertEqual(str(updated_student.date_of_birth), self.valid_data['date_of_birth'])

    def test_partial_update(self):
        partial_data = {'first_name': 'Jane'}
        serializer = StudentUpdateSerializer(self.student, data=partial_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_student = serializer.save()

        self.assertEqual(updated_student.first_name, 'Jane')
        self.assertEqual(updated_student.last_name, 'Doe')


class StudentCreateSerializerTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            role='student'
        )
        self.valid_data = {
            'user': self.user.id,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'new@example.com',
            'phone_number': '123456789',
            'date_of_birth': '2000-01-01'

        }

    def test_serializer_valid_data(self):
        serializer = StudentCreateSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())


    def test_serializer_missing_required_field(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop('email')
        serializer = StudentCreateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)


    def test_serializer_invalid_email(self):
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'invalid-email'
        serializer = StudentCreateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)


class ClassSerializerTests(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='instructor@example.com',
            specialization='Salsa'
        )
        self.class_data = {
            'name': 'Salsa Beginners',
            'style': 'Salsa',
            'max_participants': 10,
            'start_time': timezone.now(),
            'end_time': timezone.now() + timedelta(hours=1),
            'days_of_week': 'MO,WE',
            'is_recurring': True,
            'room': 'Room 1'
        }

    def test_class_detail_serializer(self):
        dance_class = Class.objects.create(instructor=self.instructor, **self.class_data)
        serializer = ClassDetailSerializer(dance_class)
        self.assertEqual(serializer.data['name'], self.class_data['name'])
        self.assertEqual(serializer.data['instructor'],
                         f"{self.instructor.first_name} {self.instructor.last_name}")
        self.assertEqual(serializer.data['available_slots'], 10)


class ClassCreateSerializerTests(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='instructor@example.com',
            specialization='Salsa'
        )
        self.valid_data = {
            'name': 'Salsa Beginners',
            'style': 'Salsa',
            'max_participants': 10,
            'instructor': self.instructor.id,
            'start_time': timezone.now(),
            'end_time': timezone.now() + timedelta(hours=1),
            'days_of_week': 'MO,WE',
            'is_recurring': True,
            'room': 'Room 1'
        }

    def test_valid_data(self):
        serializer = ClassCreateSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_missing_days_of_week_for_recurring_class(self):
        invalid_data = self.valid_data.copy()
        invalid_data['days_of_week'] = ''
        serializer = ClassCreateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('days_of_week', str(serializer.errors))

    def test_missing_required_field(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop('name')
        serializer = ClassCreateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)


class ClassUpdateSerializerTests(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='instructor@example.com',
            specialization='Salsa'
        )
        self.dance_class = Class.objects.create(
            name='Salsa Beginners',
            style='Salsa',
            max_participants=10,
            instructor=self.instructor,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            room='Room 1'
        )
        self.new_instructor = Instructor.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            specialization='Bachata'
        )
        self.valid_data = {
            'name': 'Salsa Advanced',
            'style': 'Salsa',
            'max_participants': 15,
            'instructor': self.new_instructor.id,
            'start_time': timezone.now(),
            'end_time': timezone.now() + timedelta(hours=1),
            'room': 'Room 2'
        }

    def test_update_all_fields(self):
        serializer = ClassUpdateSerializer(self.dance_class, data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        updated_class = serializer.save()

        self.assertEqual(updated_class.name, self.valid_data['name'])
        self.assertEqual(updated_class.style, self.valid_data['style'])
        self.assertEqual(updated_class.max_participants, self.valid_data['max_participants'])
        self.assertEqual(updated_class.instructor.id, self.valid_data['instructor'])
        self.assertEqual(updated_class.room, self.valid_data['room'])

    def test_partial_update(self):
        partial_data = {'name': 'New Class Name'}
        serializer = ClassUpdateSerializer(self.dance_class, data=partial_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_class = serializer.save()

        self.assertEqual(updated_class.name, 'New Class Name')
        self.assertEqual(updated_class.style, 'Salsa')


class InstructorSerializerTests(TestCase):
    def setUp(self):
        self.instructor_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com',
            'specialization': 'Salsa'
        }
        self.instructor = Instructor.objects.create(**self.instructor_data)

    def test_serializer_contains_expected_fields(self):
        serializer = InstructorSerializer(self.instructor)
        expected_fields = {'id', 'first_name', 'last_name', 'email', 'specialization'}
        self.assertEqual(set(serializer.data.keys()), expected_fields)


class InstructorCreateSerializerTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'specialization': 'Bachata'
        }

    def test_create_with_valid_data(self):
        serializer = InstructorCreateSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        instructor = serializer.save()
        self.assertEqual(instructor.first_name, self.valid_data['first_name'])
        self.assertEqual(instructor.email, self.valid_data['email'])

    def test_create_with_missing_field(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop('email')
        serializer = InstructorCreateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_create_with_invalid_email(self):
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'invalid-email'
        serializer = InstructorCreateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)


class InstructorUpdateSerializerTests(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com',
            specialization='Salsa'
        )
        self.valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'specialization': 'Bachata'
        }

    def test_update_all_fields(self):
        serializer = InstructorUpdateSerializer(self.instructor, data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        updated_instructor = serializer.save()
        self.assertEqual(updated_instructor.first_name, self.valid_data['first_name'])
        self.assertEqual(updated_instructor.specialization, self.valid_data['specialization'])

    def test_partial_update(self):
        partial_data = {'specialization': 'Tango'}
        serializer = InstructorUpdateSerializer(self.instructor, data=partial_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_instructor = serializer.save()
        self.assertEqual(updated_instructor.specialization, 'Tango')
        self.assertEqual(updated_instructor.first_name, 'Jane')


class BookingSerializerTests(TestCase):
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
            first_name='Jane',
            last_name='Smith',
            email='instructor@example.com',
            specialization='Salsa'
        )
        self.dance_class = Class.objects.create(
            name='Salsa Beginners',
            style='Salsa',
            max_participants=1,
            instructor=self.instructor,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            days_of_week='MO,WE',
            is_recurring=True,
            room='Room 1'
        )

    def test_booking_serializer_valid(self):
        data = {
            'class_model': self.dance_class.id,
            'status': 'confirmed'
        }
        serializer = BookingSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_booking_serializer_validates_max_participants(self):
        # Create first booking
        Booking.objects.create(
            student=self.student,
            class_model=self.dance_class,
            status='confirmed'
        )

        # Try to create second booking
        data = {
            'class_model': self.dance_class.id,
            'status': 'confirmed'
        }
        serializer = BookingSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('No spots available', str(serializer.errors))


class AttendanceReportSerializerTests(TestCase):
    def test_serializer_with_valid_data(self):
        data = {
            'class_name': 'Salsa Beginners',
            'instructor_name': 'Jane Smith',
            'date': timezone.now(),
            'attendance_rate': 0.75,
            'booked_slots': 8,
            'max_slots': 10
        }
        serializer = AttendanceReportSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['attendance_rate'], 0.75)
        self.assertEqual(serializer.data['booked_slots'], 8)

    def test_serializer_with_invalid_data(self):
        data = {
            'class_name': 'Salsa Beginners',
            'instructor_name': 'Jane Smith',
            'date': 'invalid-date',
            'attendance_rate': 'invalid',
            'booked_slots': 'invalid',
            'max_slots': 10
        }
        serializer = AttendanceReportSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('date', serializer.errors)
        self.assertIn('attendance_rate', serializer.errors)


class ClassAnalyticsSerializerTests(TestCase):
    def test_serializer_with_valid_data(self):
        data = {
            'popular_classes': [
                {'name': 'Salsa', 'count': 50},
                {'name': 'Bachata', 'count': 30}
            ],
            'peak_hours': [
                {'hour': 18, 'count': 25},
                {'hour': 19, 'count': 35}
            ],
            'style_distribution': [
                {'style': 'Salsa', 'percentage': 60},
                {'style': 'Bachata', 'percentage': 40}
            ]
        }
        serializer = ClassAnalyticsSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(len(serializer.data['popular_classes']), 2)
        self.assertEqual(len(serializer.data['peak_hours']), 2)


class PaymentSerializerTests(TestCase):
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
            'student': self.student.id,
            'amount': '100.00',
            'payment_type': 'single',
            'payment_method': 'cash'
        }

    def test_serializer_with_valid_data(self):
        serializer = PaymentSerializer(data=self.payment_data)
        self.assertTrue(serializer.is_valid())

    def test_read_only_fields(self):
        invalid_data = self.payment_data.copy()
        invalid_data['status'] = 'completed'
        invalid_data['paid_at'] = timezone.now()
        serializer = PaymentSerializer(data=invalid_data)
        self.assertTrue(serializer.is_valid())
        payment = serializer.save()
        self.assertEqual(payment.status, 'pending')  # Default value
        self.assertIsNone(payment.paid_at)  # Should remain None


class SchoolInfoSerializerTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'name': 'Dance Studio',
            'address': 'Test Street 123',
            'phone': '123456789',
            'email': 'contact@studio.com',
            'bank_name': 'Test Bank',
            'bank_account': '1234567890',
            'bank_recipient': 'Dance Studio Ltd',
            'transfer_title_prefix': 'Payment - '
        }

    def test_serializer_with_valid_data(self):
        serializer = SchoolInfoSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        school_info = serializer.save()
        self.assertEqual(school_info.name, self.valid_data['name'])
        self.assertEqual(school_info.email, self.valid_data['email'])


class AttendanceSerializerTests(TestCase):
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
            first_name='Jane',
            last_name='Smith',
            email='instructor@example.com',
            specialization='Salsa'
        )
        self.dance_class = Class.objects.create(
            name='Salsa Beginners',
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
        self.booking = Booking.objects.create(
            student=self.student,
            class_model=self.dance_class,
            status='confirmed'
        )

    def test_attendance_serializer_fields(self):
        serializer = AttendanceSerializer(self.attendance)
        expected_fields = {'id', 'student', 'status', 'is_booked',
                           'booking_status', 'notes', 'created_at'}
        self.assertEqual(set(serializer.data.keys()), expected_fields)

    def test_get_booking_status(self):
        serializer = AttendanceSerializer(self.attendance)
        self.assertEqual(serializer.data['booking_status'], 'confirmed')

    def test_get_booking_status_no_booking(self):
        self.booking.delete()
        serializer = AttendanceSerializer(self.attendance)
        self.assertIsNone(serializer.data['booking_status'])
