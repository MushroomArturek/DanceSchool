# test_permissions.py
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from ..permissions import IsStudent, IsInstructor, IsAdmin
from ..models import CustomUser


class PermissionTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.student = CustomUser.objects.create_user(
            email='student@example.com',
            password='testpass123',
            role='student'
        )
        self.instructor = CustomUser.objects.create_user(
            email='instructor@example.com',
            password='testpass123',
            role='instructor'
        )
        self.admin = CustomUser.objects.create_user(
            email='admin@example.com',
            password='testpass123',
            role='admin'
        )

    def test_student_permission(self):
        request = self.factory.get('/')
        request.user = self.student
        self.assertTrue(IsStudent().has_permission(request, None))
        request.user = self.instructor
        self.assertFalse(IsStudent().has_permission(request, None))

    def test_instructor_permission(self):
        request = self.factory.get('/')
        request.user = self.instructor
        self.assertTrue(IsInstructor().has_permission(request, None))
        request.user = self.student
        self.assertFalse(IsInstructor().has_permission(request, None))

    def test_admin_permission(self):
        request = self.factory.get('/')
        request.user = self.admin
        self.assertTrue(IsAdmin().has_permission(request, None))
        request.user = self.student
        self.assertFalse(IsAdmin().has_permission(request, None))

    def test_unauthenticated_request(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        self.assertFalse(IsStudent().has_permission(request, None))
        self.assertFalse(IsInstructor().has_permission(request, None))
        self.assertFalse(IsAdmin().has_permission(request, None))

    def test_different_role_combinations(self):
        request = self.factory.get('/')

        request.user = self.student
        self.assertTrue(IsStudent().has_permission(request, None))
        self.assertFalse(IsInstructor().has_permission(request, None))
        self.assertFalse(IsAdmin().has_permission(request, None))

        request.user = self.instructor
        self.assertFalse(IsStudent().has_permission(request, None))
        self.assertTrue(IsInstructor().has_permission(request, None))
        self.assertFalse(IsAdmin().has_permission(request, None))

        request.user = self.admin
        self.assertFalse(IsStudent().has_permission(request, None))
        self.assertFalse(IsInstructor().has_permission(request, None))
        self.assertTrue(IsAdmin().has_permission(request, None))

    def test_inactive_user(self):
        request = self.factory.get('/')
        inactive_user = CustomUser.objects.create_user(
            email='inactive@example.com',
            password='testpass123',
            role='student',
            is_active=False
        )
        request.user = inactive_user
        self.assertFalse(IsStudent().has_permission(request, None))
        self.assertFalse(IsInstructor().has_permission(request, None))
        self.assertFalse(IsAdmin().has_permission(request, None))

    def test_anonymous_user(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        self.assertFalse(IsStudent().has_permission(request, None))
        self.assertFalse(IsInstructor().has_permission(request, None))
        self.assertFalse(IsAdmin().has_permission(request, None))
