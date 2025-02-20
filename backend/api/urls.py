from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView, RegisterUserView, StudentProfileView, StudentProfileUpdateView, \
    AttendanceReportView, ClassAnalyticsView, PaymentListView, PaymentDetailView, PaymentCreateView, PaymentUpdateView, \
    PaymentDeleteView, SchoolInfoView, SchoolInfoUpdateView, AttendanceListView, AttendanceDetailView
from .views import (
    StudentListView,
    StudentDetailView,
    StudentCreateView,
    StudentUpdateView,
    StudentDeleteView,
    ClassListView,
    ClassDetailView,
    ClassCreateView,
    ClassUpdateView,
    ClassDeleteView,
    InstructorListView,
    InstructorDetailView,
    InstructorCreateView,
    InstructorUpdateView,
    InstructorDeleteView,
    BookingListView,
    BookingCreateView,
    BookingDetailView,
    BookingDeleteView,
)

urlpatterns = [
    # Endpoints dla Students
    path("students/", StudentListView.as_view(), name="student-list"),
    path("students/<int:id>/", StudentDetailView.as_view(), name="student-detail"),
    path("students/create/", StudentCreateView.as_view(), name="student-create"),
    path("students/<int:id>/update/", StudentUpdateView.as_view(), name="student-update"),
    path("students/<int:id>/delete/", StudentDeleteView.as_view(), name="student-delete"),

    # Endpoints dla Classes
    path("classes/", ClassListView.as_view(), name="class-list"),
    path("classes/<int:id>/", ClassDetailView.as_view(), name="class-detail"),
    path("classes/create/", ClassCreateView.as_view(), name="class-create"),
    path("classes/<int:id>/update/", ClassUpdateView.as_view(), name="class-update"),
    path("classes/<int:id>/delete/", ClassDeleteView.as_view(), name="class-delete"),

    # Endpoints dla Instructors
    path("instructors/", InstructorListView.as_view(), name="instructor-list"),  # /api/instructors/
    path("instructors/<int:id>/", InstructorDetailView.as_view(), name="instructor-detail"),  # /api/instructors/<id>/
    path("instructors/create/", InstructorCreateView.as_view(), name="instructor-create"),  # /api/instructors/create/
    path("instructors/<int:id>/update/", InstructorUpdateView.as_view(), name="instructor-update"),
    path("instructors/<int:id>/delete/", InstructorDeleteView.as_view(), name="instructor-delete"),

    # Endpoints dla Bookings
    path("bookings/", BookingListView.as_view(), name="booking-list"),
    path("bookings/create/", BookingCreateView.as_view(), name="booking-create"),
    path("bookings/<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
    path("bookings/<int:pk>/delete/", BookingDeleteView.as_view(), name="booking-delete"),

    # Endpointy auth
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterUserView.as_view(), name='register'),

    # Student profile endpoints
    path("student/profile/", StudentProfileView.as_view(), name="student-profile"),
    path("student/profile/update/", StudentProfileUpdateView.as_view(), name="student-profile-update"),

    # Report endpoints
    path('reports/attendance/<str:period>/', AttendanceReportView.as_view(), name='attendance-report'),
    path('reports/analytics/<str:period>/', ClassAnalyticsView.as_view(), name='class-analytics'),

    ## Payments endpoints
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
    path('payments/create/', PaymentCreateView.as_view(), name='payment-create'),
    path('payments/<int:pk>/update/', PaymentUpdateView.as_view(), name='payment-update'),
    path('payments/<int:pk>/delete/', PaymentDeleteView.as_view(), name='payment-delete'),

    # School info endpoints
    path('school-info/', SchoolInfoView.as_view(), name='school-info'),
    path('school-info/update/', SchoolInfoUpdateView.as_view(), name='school-info-update'),

    # Attendance endpoints
    path('classes/<int:class_id>/attendance/', AttendanceListView.as_view(), name='attendance-list'),
    path('classes/<int:class_id>/attendance/<int:student_id>/', AttendanceDetailView.as_view(), name='attendance-detail'),
]

