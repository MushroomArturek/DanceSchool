from rest_framework import serializers
from .models import Student, Class, Instructor, Booking, CustomUser


# Auth

class CustomTokenObtainPairSerializer(serializers.Serializer):
    # Pole dla tokenów JWT
    access = serializers.CharField()
    refresh = serializers.CharField()

    # Pola, które chcesz dodać do odpowiedzi
    role = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def validate(self, attrs):
        # Tylko, jeśli standardowy serializer poprawnie przetworzył dane
        data = super().validate(attrs)
        user = CustomUser.objects.get(email=attrs["email"])

        # Dodajemy dane użytkownika do odpowiedzi
        data["role"] = user.role
        data["first_name"] = user.first_name
        data["last_name"] = user.last_name

        return data

class RegisterUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)  # Dane studenta
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name', 'phone_number', 'date_of_birth']
        extra_kwargs = {'password': {'write_only': True}}  # Hasło zapisujemy tylko w modelu "CustomUser"

    def create(self, validated_data):
        # Oddzielamy dane użytkownika i studenta
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        phone_number = validated_data.pop('phone_number')
        date_of_birth = validated_data.pop('date_of_birth')

        # Tworzymy użytkownika
        user = CustomUser.objects.create_user(role='student', **validated_data)

        # Tworzymy studenta i wiążemy go z użytkownikiem
        Student.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=user.email,  # Student ma ten sam email co użytkownik
            phone_number=phone_number,
            date_of_birth=date_of_birth
        )
        return user
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'  # Serializuj wszystkie pola modelu


class StudentUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)

    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "date_of_birth",
        ]

    def update(self, instance, validated_data):
        # Aktualizujemy pola studenta
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.save()
        return instance

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
    instructor = serializers.PrimaryKeyRelatedField(queryset=Instructor.objects.all())
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
    instructor = serializers.PrimaryKeyRelatedField(queryset=Instructor.objects.all())

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

