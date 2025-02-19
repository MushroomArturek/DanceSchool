from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Student, Class, Instructor, Booking, CustomUser, Payment


# Auth

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Dodajemy rolę do tokena
        token['role'] = user.role
        return token


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
    class Meta:
        model = Class
        fields = [
            "name",
            "style",
            "max_participants",
            "instructor",
            "start_time",
            "end_time",
            "days_of_week",
            "is_recurring",
            "room",
        ]

    def validate(self, data):
        if data.get('is_recurring') and not data.get('days_of_week'):
            raise serializers.ValidationError("Dla zajęć cyklicznych wymagane jest pole days_of_week")
        return data


class ClassDetailSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    instructor = serializers.SerializerMethodField()
    available_slots = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = "__all__"

    def get_instructor(self, obj):
        return f"{obj.instructor.first_name} {obj.instructor.last_name}"

    def get_available_slots(self, obj):
        booked_count = obj.bookings.filter(status="confirmed").count()
        return obj.max_participants - booked_count


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
    class_details = ClassDetailSerializer(source='class_model', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'student', 'class_model', 'class_details', 'booking_date', 'status']
        read_only_fields = ['student', 'booking_date']

    def validate(self, data):
        class_instance = data['class_model']
        if class_instance.bookings.filter(status="confirmed").count() >= class_instance.max_participants:
            raise serializers.ValidationError("No spots available for this class.")
        return data

# Reports

class AttendanceReportSerializer(serializers.Serializer):
    class_name = serializers.CharField()
    instructor_name = serializers.CharField()
    date = serializers.DateTimeField()
    attendance_rate = serializers.FloatField()
    booked_slots = serializers.IntegerField()
    max_slots = serializers.IntegerField()

class ClassAnalyticsSerializer(serializers.Serializer):
    popular_classes = serializers.ListField(child=serializers.DictField())
    peak_hours = serializers.ListField(child=serializers.DictField())
    style_distribution = serializers.ListField(child=serializers.DictField())

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'student', 'amount', 'payment_type', 'status',
                 'created_at', 'paid_at', 'valid_until']
        read_only_fields = ['status', 'paid_at', 'valid_until']
