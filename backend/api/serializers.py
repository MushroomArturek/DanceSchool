from rest_framework import serializers
from .models import Student, Class, Instructor, Booking, CustomUser


# Auth

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'  # Serializuj wszystkie pola modelu

class StudentUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = Student
        fields = [
            "email",
            "phone_number",
        ]

class StudentCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
        ]

class ClassCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    style = serializers.CharField(required=True)
    max_participants = serializers.IntegerField(required=True)
    instructor = serializers.CharField(required=True)
    start_time = serializers.DateTimeField(required=True)
    end_time = serializers.DateTimeField(required=True)

    class Meta:
        model = Class
        fields = [
            "name",
            "style",
            "max_participants",
            "instructor",
            "start_time",
            "end_time",
            "room",
        ]

class ClassUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    style = serializers.CharField(required=False)
    max_participants = serializers.IntegerField(required=False)
    instructor = serializers.CharField(required=False)

    class Meta:
        model = Class
        fields = [
            "name",
            "style",
            "max_participants",
            "instructor",
            "start_time",
            "end_time",
            "room",
        ]

class ClassDetailSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Class
        fields = "__all__"


class InstructorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['first_name', 'last_name', 'email', 'specialization']


class InstructorUpdateSerializer(serializers.ModelSerializer):
    specialization = serializers.CharField(required=False)

    class Meta:
        model = Instructor
        fields = ['first_name', 'last_name', 'email', 'specialization']


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'student', 'class_model', 'booking_date', 'status']
        read_only_fields = ['student', 'booking_date', 'status']

    def validate(self, data):
        """
        Sprawdź, czy na te zajęcia są dostępne miejsca.
        """
        class_instance = data['class_model']
        if class_instance.bookings.filter(status="confirmed").count() >= class_instance.max_participants:
            raise serializers.ValidationError("Brak wolnych miejsc na te zajęcia.")
        return data

