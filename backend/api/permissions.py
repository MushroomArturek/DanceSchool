from rest_framework import permissions

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and request.user.is_active 
            and request.user.role == "student"
        )

class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and request.user.is_active 
            and request.user.role == "instructor"
        )

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and request.user.is_active 
            and request.user.role == "admin"
        )