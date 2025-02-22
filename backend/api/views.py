from datetime import timedelta

from django.db.models import Count, FloatField, F
from django.db.models.functions import Cast, ExtractHour
from django.utils import timezone
from rest_framework.exceptions import NotFound
from rest_framework import generics, status, serializers, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Student, Instructor, Class, Booking, CustomUser, Payment, SchoolInfo, Attendance
from .permissions import IsAdmin
from .serializers import StudentSerializer, StudentUpdateSerializer, StudentCreateSerializer, InstructorSerializer, \
    InstructorCreateSerializer, InstructorUpdateSerializer, ClassDetailSerializer, ClassCreateSerializer, \
    ClassUpdateSerializer, BookingSerializer, RegisterUserSerializer, CustomTokenObtainPairSerializer, \
    AttendanceReportSerializer, ClassAnalyticsSerializer, PaymentSerializer, SchoolInfoSerializer, AttendanceSerializer


# Auth (Pierwsza klasa do serializers?????)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        email = request.data.get("email")
        user = CustomUser.objects.filter(email=email).first()

        if user:
            # Changed to match frontend expectations
            user_data = {
                "email": user.email,  # Add email
                "firstName": user.first_name,
                "lastName": user.last_name,
                "role": user.role,
            }
            response.data.update(user_data)

        return response


class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": {
                "email": user.email,
                "role": user.role,
            },
            "student": {
                "first_name": user.student.first_name,
                "last_name": user.student.last_name,
                "email": user.student.email,
                "phone_number": user.student.phone_number,
                "date_of_birth": user.student.date_of_birth,
            }
        }, status=status.HTTP_201_CREATED)


class StudentDeleteView(generics.DestroyAPIView):
    model = Student

    def get_object(self):
        try:
            return Student.objects.get(pk=self.kwargs["id"])
        except Student.DoesNotExist:
            raise NotFound(detail="Student not found.")


class StudentListView(generics.ListAPIView):
    model = Student
    serializer_class = StudentSerializer

    def get_queryset(self):
        # Możesz dodać tutaj filtrowanie
        return Student.objects.all()


class StudentUpdateView(generics.UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Pobieramy studenta powiązanego z użytkownikiem (używamy usera zalogowanego w request)
        try:
            return Student.objects.get(user=self.request.user)  # Powiązany student z zalogowanym użytkownikiem
        except Student.DoesNotExist:
            raise NotFound(detail="Student not found.")


class StudentCreateView(generics.CreateAPIView):
    model = Student
    serializer_class = StudentCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class StudentDetailView(generics.RetrieveAPIView):
    model = Student
    serializer_class = StudentSerializer

    def get_object(self):
        try:
            return Student.objects.get(pk=self.kwargs["id"])
        except Student.DoesNotExist:
            raise NotFound(detail="Student not found.")


class StudentProfileView(generics.RetrieveAPIView):
    """ Endpoint zwracający dane studenta powiązanego z zalogowanym użytkownikiem """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            raise NotFound(detail="Student not found.")


class StudentProfileUpdateView(generics.UpdateAPIView):
    """ Endpoint do aktualizacji danych studenta """
    serializer_class = StudentUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """ Pobiera studenta powiązanego z użytkownikiem """
        try:
            return Student.objects.get(user=self.request.user)
        except Student.DoesNotExist:
            raise NotFound(detail="Student not found.")


class InstructorListView(generics.ListAPIView):
    queryset = Instructor.objects.all()

    serializer_class = InstructorSerializer
    permission_classes = [IsAuthenticated,
                          IsAdmin]  # Add permissions  class InstructorDetailView(generics.RetrieveAPIView): queryset = Instructor.objects.all() serializer_class = InstructorSerializer

    def get_object(self):
        try:
            return Instructor.objects.get(pk=self.kwargs['id'])
        except Instructor.DoesNotExist:
            raise NotFound(detail="Instructor not found.")


class InstructorDetailView(generics.RetrieveAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

    def get_object(self):
        try:
            return Instructor.objects.get(pk=self.kwargs['id'])
        except Instructor.DoesNotExist:
            raise NotFound(detail="Instructor not found.")


class InstructorCreateView(generics.CreateAPIView):
    serializer_class = InstructorCreateSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        return Response(InstructorSerializer(instance).data, status=status.HTTP_201_CREATED)


class InstructorUpdateView(generics.UpdateAPIView):
    queryset = Instructor.objects.all()

    serializer_class = InstructorUpdateSerializer

    def get_object(self):
        try:
            return Instructor.objects.get(pk=self.kwargs['id'])
        except Instructor.DoesNotExist:
            raise NotFound(detail="Instructor not found.")


class InstructorDeleteView(generics.DestroyAPIView):
    queryset = Instructor.objects.all()

    def get_object(self):
        try:
            return Instructor.objects.get(pk=self.kwargs['id'])
        except Instructor.DoesNotExist:
            raise NotFound(detail="Instructor not found.")


class ClassListView(generics.ListAPIView):
    model = Class
    serializer_class = ClassDetailSerializer
    permission_classes = []  # Allow unauthenticated access

    def get_queryset(self):
        queryset = Class.objects.all()
        style = self.request.query_params.get("style", None)
        if style:
            queryset = queryset.filter(style__icontains=style)
        return queryset


class ClassDetailView(generics.RetrieveAPIView):
    model = Class
    serializer_class = ClassDetailSerializer
    permission_classes = []  # Allow unauthenticated access

    def get_object(self):
        try:
            return Class.objects.get(pk=self.kwargs["id"])
        except Class.DoesNotExist:
            raise NotFound(detail="Class not found.")


class ClassCreateView(generics.CreateAPIView):
    model = Class
    serializer_class = ClassCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        return Response(ClassDetailSerializer(instance).data, status=status.HTTP_201_CREATED)


class ClassUpdateView(generics.UpdateAPIView):
    model = Class
    serializer_class = ClassUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Class.objects.get(pk=self.kwargs["id"])
        except Class.DoesNotExist:
            raise NotFound(detail="Class not found.")


class ClassDeleteView(generics.DestroyAPIView):
    model = Class
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Class.objects.get(pk=self.kwargs["id"])
        except Class.DoesNotExist:
            raise NotFound(detail="Class not found.")


class BookingListView(generics.ListAPIView):
    """
    GET: Returns list of bookings for logged in user.
    """
    model = Booking
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter bookings for currently logged in user's student profile
        """
        try:
            student = Student.objects.get(user=self.request.user)
            return Booking.objects.filter(student=student)
        except Student.DoesNotExist:
            return Booking.objects.none()


class BookingCreateView(generics.CreateAPIView):
    """
    POST: Create new booking for user.
    """
    model = Booking
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            student = Student.objects.get(user=self.request.user)
            class_instance = serializer.validated_data["class_model"]

            # Check if spots available
            if class_instance.bookings.filter(status="confirmed").count() >= class_instance.max_participants:
                raise serializers.ValidationError("No spots available for this class.")

            # Create booking
            serializer.save(student=student)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Student profile not found.")


class BookingDetailView(generics.RetrieveAPIView):
    """
    GET: Pobierz szczegóły dotyczące konkretnej rezerwacji.
    """
    model = Booking
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter bookings for currently logged in user's student profile
        """
        try:
            student = Student.objects.get(user=self.request.user)
            return Booking.objects.filter(student=student)
        except Student.DoesNotExist:
            return Booking.objects.none()


class BookingDeleteView(generics.DestroyAPIView):
    """
    DELETE: Usuń (anuluj) rezerwację użytkownika.
    """
    model = Booking
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return Booking.objects.filter(student=student)
        except Student.DoesNotExist:
            return Booking.objects.none()

    def perform_destroy(self, instance):
        instance.status = "cancelled"
        instance.save()


# Reports

class AttendanceReportView(generics.ListAPIView):
    """
    GET: Returns attendance statistics for classes
    """
    serializer_class = AttendanceReportSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        period = self.kwargs.get('period', 'month')
        end_date = timezone.now()

        if period == 'week':
            start_date = end_date - timedelta(days=7)
        elif period == 'month':
            start_date = end_date - timedelta(days=30)
        else:  # quarter
            start_date = end_date - timedelta(days=90)

        return (
            Booking.objects
            .filter(class_model__start_time__range=(start_date, end_date))
            .values(
                'class_model__name',
                'class_model__instructor__first_name',
                'class_model__instructor__last_name',
                'class_model__start_time',
                'class_model__max_participants'
            )
            .annotate(
                class_name=F('class_model__name'),
                instructor_name=F('class_model__instructor__first_name'),
                date=F('class_model__start_time'),
                booked_slots=Count('id'),
                max_slots=F('class_model__max_participants'),
                attendance_rate=Cast(
                    Count('id') * 100.0 / F('class_model__max_participants'),
                    FloatField()
                )
            )
            .order_by('-class_model__start_time')
        )


class ClassAnalyticsView(generics.RetrieveAPIView):
    """
    GET: Returns analytics data for classes
    """
    serializer_class = ClassAnalyticsSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self):
        period = self.kwargs.get('period', 'month')
        end_date = timezone.now()

        if period == 'month':
            start_date = end_date - timedelta(days=30)
        elif period == 'quarter':
            start_date = end_date - timedelta(days=90)
        else:  # year
            start_date = end_date - timedelta(days=365)

        # Popular classes
        popular_classes = (
            Class.objects
            .filter(start_time__range=(start_date, end_date))
            .annotate(booking_count=Count('bookings'))
            .values('name', 'booking_count')
            .order_by('-booking_count')[:5]
        )

        # Peak hours
        peak_hours = (
            Class.objects
            .filter(start_time__range=(start_date, end_date))
            .annotate(hour=ExtractHour('start_time'))
            .values('hour')
            .annotate(class_count=Count('id'))
            .order_by('hour')
        )

        # Style distribution
        style_distribution = (
            Class.objects
            .filter(start_time__range=(start_date, end_date))
            .values('style')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        return {
            'popular_classes': popular_classes,
            'peak_hours': peak_hours,
            'style_distribution': style_distribution
        }


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


class PaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


class PaymentUpdateView(generics.UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


class PaymentDeleteView(generics.DestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


class SchoolInfoMixin:
    """
    Mixin zapewniający istnienie pojedynczej encji SchoolInfo
    """

    def get_object(self):
        school_info = SchoolInfo.objects.first()
        if not school_info:
            # Create default SchoolInfo if none exists
            school_info = SchoolInfo.objects.create(
                name="Szkoła Tańca",
                address="Ulica przykładowa 1",
                phone="000000000",
                email="kontakt@szkola.pl",
                bank_name="Bank",
                bank_account="00 0000 0000 0000 0000 0000 0000",
                bank_recipient="Szkoła Tańca",
                transfer_title_prefix="Płatność - "
            )
        return school_info


class SchoolInfoView(SchoolInfoMixin, generics.RetrieveAPIView):
    """
    GET: Returns the school information
    """
    serializer_class = SchoolInfoSerializer
    permission_classes = []  # Allow public access


class SchoolInfoUpdateView(SchoolInfoMixin, generics.UpdateAPIView):
    """
    PUT/PATCH: Updates the school information
    """
    serializer_class = SchoolInfoSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class AttendanceListView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        class_id = self.kwargs['class_id']
        # First verify class exists
        if not Class.objects.filter(id=class_id).exists():
            raise NotFound(detail="Class not found.")
        return Attendance.objects.filter(class_instance_id=class_id)

    def perform_create(self, serializer):
        class_id = self.kwargs['class_id']
        try:
            class_instance = Class.objects.get(id=class_id)
            serializer.save(class_instance=class_instance)
        except Class.DoesNotExist:
            raise NotFound(detail="Class not found.")


class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        class_id = self.kwargs['class_id']
        student_id = self.kwargs['student_id']
        try:
            return Attendance.objects.get(
                class_instance_id=class_id,
                student_id=student_id
            )
        except Attendance.DoesNotExist:
            raise NotFound(detail="Attendance record not found.")


