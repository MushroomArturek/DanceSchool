from django.contrib.auth.models import AbstractUser
from django.db import models


# Auth

# Definicja możliwych ról użytkowników
class Role(models.TextChoices):
    GUEST = "guest", "Gość"
    STUDENT = "student", "Uczeń"
    INSTRUCTOR = "instructor", "Instruktor"
    ADMIN = "admin", "Administrator"


class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=Role.GUEST,
        help_text="Rola użytkownika w systemie",
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Class(models.Model):
    name = models.CharField(max_length=200)
    style = models.CharField(max_length=100, help_text="Styl tańca (np. Salsa, Waltz)")
    max_participants = models.PositiveIntegerField(help_text="Maksymalna liczba uczestników")
    instructor = models.CharField(max_length=200, help_text="Imię i nazwisko nauczyciela")
    start_time = models.DateTimeField(help_text="Data i czas rozpoczęcia zajęć")
    end_time = models.DateTimeField(help_text="Data i czas zakończenia zajęć")
    room = models.CharField(max_length=50, help_text="Sala zajęciowa", blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.style})"

    def available_slots(self):
        """
        Oblicza wolne miejsca na zajęciach.
        """
        booked_count = self.bookings.filter(status="confirmed").count()  # Liczba potwierdzonych rezerwacji
        return self.max_participants - booked_count


class Instructor(models.Model):
    first_name = models.CharField(max_length=50, help_text="Imię instruktora")
    last_name = models.CharField(max_length=50, help_text="Nazwisko instruktora")
    email = models.EmailField(unique=True, help_text="E-mail kontaktowy")
    specialization = models.CharField(max_length=100, help_text="Specjalizacja (np. Salsa, Tango)", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.specialization}"

class Booking(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                related_name="bookings")  # Powiązanie z użytkownikiem
    class_model = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="bookings")  # Powiązanie z zajęciami
    booking_date = models.DateTimeField(auto_now_add=True)  # Czas rezerwacji
    status = models.CharField(
        max_length=20,
        choices=[("confirmed", "Potwierdzona"), ("cancelled", "Anulowana"), ("waiting", "Oczekująca")],
        default="confirmed"
    )

    class Meta:
        unique_together = ['student', 'class_model']  # Użytkownik może zarezerwować dane zajęcia tylko raz

    def __str__(self):
        return f"{self.student} - {self.class_model} ({self.status})"


