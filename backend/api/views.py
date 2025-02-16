from rest_framework.exceptions import NotFound
from rest_framework import generics, status, serializers, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Student, Instructor, Class, Booking, CustomUser
from .serializers import StudentSerializer, StudentUpdateSerializer, StudentCreateSerializer, InstructorSerializer, \
    InstructorCreateSerializer, InstructorUpdateSerializer, ClassDetailSerializer, ClassCreateSerializer, \
    ClassUpdateSerializer, BookingSerializer, RegisterUserSerializer, CustomTokenObtainPairSerializer


# Auth (Pierwsza klasa do serializers?????)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # Uzyskujemy token
        response = super().post(request, *args, **kwargs)

        # Pobieramy użytkownika na podstawie adresu email
        email = request.data.get("email")
        user = CustomUser.objects.filter(email=email).first()

        if user:
            # Dodajemy dane użytkownika do odpowiedzi
            user_data = {
                "firstName": user.first_name,
                "lastName": user.last_name,
                "role": user.role,
            }
            response.data.update(user_data)

        return response

class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": {
                "email": user.email,
                "role": user.role,
            },
            "student": {
                "first_name": user.student.first_name,
                "last_name": user.student.last_name,
                "email": user.student.email,
                "phone_number": user.student.phone_number,
                "date_of_birth": user.student.date_of_birth,
            }
        }, status=status.HTTP_201_CREATED)




class StudentDeleteView(generics.DestroyAPIView):
    model = Student

    def get_object(self):
        try:
            return Student.objects.get(pk=self.kwargs["id"])
        except Student.DoesNotExist:
            raise NotFound(detail="Student not found.")

class StudentListView(generics.ListAPIView):
    model = Student
    serializer_class = StudentSerializer

    def get_queryset(self):
        # Możesz dodać tutaj filtrowanie
        return Student.objects.all()


class StudentUpdateView(generics.UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Pobieramy studenta powiązanego z użytkownikiem (używamy usera zalogowanego w request)
        try:
            return Student.objects.get(user=self.request.user)  # Powiązany student z zalogowanym użytkownikiem
        except Student.DoesNotExist:
            raise NotFound(detail="Student not found.")


class StudentCreateView(generics.CreateAPIView):
    model = Student
    serializer_class = StudentCreateSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        # Możesz zmienić serializer do zwracania szczegółowych danych
        return Response(StudentSerializer(instance).data, status=status.HTTP_201_CREATED)

class StudentDetailView(generics.RetrieveAPIView):
    model = Student
    serializer_class = StudentSerializer

    def get_object(self):
        try:
            return Student.objects.get(pk=self.kwargs["id"])
        except Student.DoesNotExist:
            raise NotFound(detail="Student not found.")


class StudentProfileView(generics.RetrieveAPIView):
    """ Endpoint zwracający dane studenta powiązanego z zalogowanym użytkownikiem """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            raise NotFound(detail="Student not found.")

class StudentProfileUpdateView(generics.UpdateAPIView):
    """ Endpoint do aktualizacji danych studenta """
    serializer_class = StudentUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """ Pobiera studenta powiązanego z użytkownikiem """
        try:
            return Student.objects.get(user=self.request.user)
        except Student.DoesNotExist:
            raise NotFound(detail="Student not found.")


class InstructorListView(generics.ListAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer


class InstructorDetailView(generics.RetrieveAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

    def get_object(self):
        try:
            return Instructor.objects.get(pk=self.kwargs['id'])
        except Instructor.DoesNotExist:
            raise NotFound(detail="Instructor not found.")


class InstructorCreateView(generics.CreateAPIView):
    serializer_class = InstructorCreateSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        return Response(InstructorSerializer(instance).data, status=status.HTTP_201_CREATED)


class InstructorUpdateView(generics.UpdateAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorUpdateSerializer

    def get_object(self):
        try:
            return Instructor.objects.get(pk=self.kwargs['id'])
        except Instructor.DoesNotExist:
            raise NotFound(detail="Instructor not found.")


class InstructorDeleteView(generics.DestroyAPIView):
    queryset = Instructor.objects.all()

    def get_object(self):
        try:
            return Instructor.objects.get(pk=self.kwargs['id'])
        except Instructor.DoesNotExist:
            raise NotFound(detail="Instructor not found.")

class ClassListView(generics.ListAPIView):
    model = Class
    serializer_class = ClassDetailSerializer

    def get_queryset(self):
        queryset = Class.objects.all()
        # Dodaj opcjonalne filtrowanie np. po stylu zajęć
        style = self.request.query_params.get("style", None)
        if style:
            queryset = queryset.filter(style__icontains=style)
        return queryset

class ClassDetailView(generics.RetrieveAPIView):
    model = Class
    serializer_class = ClassDetailSerializer

    def get_object(self):
        try:
            return Class.objects.get(pk=self.kwargs["id"])
        except Class.DoesNotExist:
            raise NotFound(detail="Class not found.")

class ClassCreateView(generics.CreateAPIView):
    model = Class
    serializer_class = ClassCreateSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        return Response(ClassDetailSerializer(instance).data, status=status.HTTP_201_CREATED)

class ClassUpdateView(generics.UpdateAPIView):
    model = Class
    serializer_class = ClassUpdateSerializer

    def get_object(self):
        try:
            return Class.objects.get(pk=self.kwargs["id"])
        except Class.DoesNotExist:
            raise NotFound(detail="Class not found.")

class ClassDeleteView(generics.DestroyAPIView):
    model = Class

    def get_object(self):
        try:
            return Class.objects.get(pk=self.kwargs["id"])
        except Class.DoesNotExist:
            raise NotFound(detail="Class not found.")

class BookingListView(generics.ListAPIView):
    """
    GET: Zwraca listę rezerwacji dla zalogowanego użytkownika.
    """
    model = Booking
    serializer_class = BookingSerializer

    def get_queryset(self):
        """
        Filtruje rezerwacje dla aktualnie zalogowanego użytkownika.
        """
        return Booking.objects.filter(student=self.request.user)

class BookingCreateView(generics.CreateAPIView):
    """
    POST: Tworzenie nowej rezerwacji dla użytkownika.
    """
    model = Booking
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        """
        Sprawdź dostępność miejsc przed stworzeniem rezerwacji.
        """
        class_instance = serializer.validated_data["class_model"]

        # Sprawdzenie, czy są dostępne miejsca
        if class_instance.bookings.filter(status="confirmed").count() >= class_instance.max_participants:
            raise serializers.ValidationError("Brak wolnych miejsc na te zajęcia.")

        # Przypisz aktualnego użytkownika do rezerwacji
        serializer.save(student=self.request.user)

class BookingDetailView(generics.RetrieveAPIView):
    """
    GET: Pobierz szczegóły dotyczące konkretnej rezerwacji.
    """
    model = Booking
    serializer_class = BookingSerializer

    def get_queryset(self):
        """
        Pozwala użytkownikowi pobrać szczegóły wyłącznie jego własnych rezerwacji.
        """
        return Booking.objects.filter(student=self.request.user)

class BookingDeleteView(generics.DestroyAPIView):
    """
    DELETE: Usuń (anuluj) rezerwację użytkownika.
    """
    model = Booking
    serializer_class = BookingSerializer

    def get_queryset(self):
        """
        Pozwala użytkownikowi anulować wyłącznie jego własne rezerwacje.
        """
        return Booking.objects.filter(student=self.request.user)

    def perform_destroy(self, instance):
        """
        Zamiast fizycznego usunięcia, zmień status rezerwacji na 'cancelled'.
        """
        instance.status = "cancelled"
        instance.save()
