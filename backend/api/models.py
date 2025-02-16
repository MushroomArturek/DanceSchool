from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


# Auth

# Definicja możliwych ról użytkowników
class Role(models.TextChoices):
    STUDENT = "student", "Uczeń"
    INSTRUCTOR = "instructor", "Instruktor"
    ADMIN = "admin", "Administrator"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=20, choices=[('student', 'Student'), ('instructor', 'Instructor'), ('admin', 'Administrator')], default='student')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Student(models.Model):
    user = models.OneToOneField(
        'CustomUser', on_delete=models.CASCADE, related_name='student'
    )  # Student jest powiązany z jednym użytkownikiem
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()  # Dodaj pole daty urodzenia
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Class(models.Model):
    name = models.CharField(max_length=200)
    style = models.CharField(max_length=100, help_text="Styl tańca (np. Salsa, Waltz)")
    max_participants = models.PositiveIntegerField(help_text="Maksymalna liczba uczestników")
    instructor = models.ForeignKey(
        'Instructor',  # Zakładamy, że model Instructor jest w tej samej aplikacji
        on_delete=models.CASCADE,
        related_name='classes',
        help_text="Wybierz instruktora spośród istniejących"
    )
    start_time = models.DateTimeField(help_text="Data i czas rozpoczęcia zajęć")
    end_time = models.DateTimeField(help_text="Data i czas zakończenia zajęć")
    room = models.CharField(max_length=50, help_text="Sala zajęciowa", blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.style})"

    def available_slots(self):
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


