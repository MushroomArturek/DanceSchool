from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Class, Instructor, Student, Booking  # Import naszego CustomUser


admin.site.register(Class)
admin.site.register(Instructor)
admin.site.register(Student)
admin.site.register(Booking)


# Rejestracja CustomUser w Django Admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Wyświetlane kolumny w panelu listy użytkowników
    list_display = ('email', 'role', 'is_staff', 'is_active')

    # Wyszukiwarka - można wyszukiwać po tych polach
    search_fields = ('email', 'role')

    # Pola, które można edytować w panelu Admina
    fieldsets = UserAdmin.fieldsets + (
        ('Dodatkowe pola', {'fields': ('role',)}),  # Dodajemy pole "role"
    )

    # Pola wyświetlane przy tworzeniu nowego użytkownika
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Dodatkowe pola', {'fields': ('role',)}),
    )

    # Nadpisanie kolejności sortowania - zmiana na email
    ordering = ['email']
