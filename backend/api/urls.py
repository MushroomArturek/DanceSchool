from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView, RegisterUserView, StudentProfileView, StudentProfileUpdateView
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
    # /api/instructors/<id>/update/
    path("instructors/<int:id>/delete/", InstructorDeleteView.as_view(), name="instructor-delete"),
    # /api/instructors/<id>/delete/
    path("bookings/", BookingListView.as_view(), name="booking-list"),
    path("bookings/create/", BookingCreateView.as_view(), name="booking-create"),
    path("bookings/<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
    path("bookings/<int:pk>/delete/", BookingDeleteView.as_view(), name="booking-delete"),

    # Endpointy auth
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterUserView.as_view(), name='register'),

    path("student/profile/", StudentProfileView.as_view(), name="student-profile"),
    path("student/profile/update/", StudentProfileUpdateView.as_view(), name="student-profile-update"),



]

