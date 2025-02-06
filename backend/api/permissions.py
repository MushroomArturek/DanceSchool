from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    """
    Uprawnienia dla uczniów
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"


class IsInstructor(BasePermission):
    """
    Uprawnienia dla instruktorów
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "instructor"


class IsAdmin(BasePermission):
    """
    Uprawnienia dla administratorów
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"
