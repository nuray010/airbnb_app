from django.shortcuts import render
from .serializer import (UserProfileListSerializer, RulesSerializer, PropertyListSerializer,PropertyDetailSerializer, ReviewSerializer,
                         BookingSerializer,CitySerializer,UserRegisterSerializer,LoginSerializer, UserProfileDetailSerializer,
                         PropertyCreateSerializer, ReviewCreateSerializer)
from .models import (UserProfile,Property,Rules,Review,City,Booking)
from rest_framework import viewsets, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from .permissions import CheckRolePermission, CreateHotelPermission
from .filter import PropertyFilter
from .pagination import PropertyPagination
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)






class UserProfileListAPIView(generics.ListAPIView):
  queryset = UserProfile.objects.all()
  serializer_class = UserProfileListSerializer

  def get_queryset(self):
      return UserProfile.objects.filter(id=self.request.user.id)


class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = UserProfile.objects.all()
  serializer_class = UserProfileDetailSerializer

  def get_queryset(self):
      return UserProfile.objects.filter(id=self.request.user.id)

class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rules.objects.all()
    serializer_class = RulesSerializer


class PropertyListAPIView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['property_type', 'max_guests', 'city',  'rules']
    pagination_class = PropertyPagination
    ordering_fields = ['property_type', 'city', 'price']

class PropertyCreateView(generics.CreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyCreateSerializer
    permission_classes = [CreateHotelPermission]

    def get_queryset(self):
        return Property.objects.filter(host=self.request.user)


class PropertyDetailAPIView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [CheckRolePermission]

    def get_queryset(self):
        return Booking.objects.filter(guest=self.request.user)

class ReviewView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [CheckRolePermission]
    filterset_fields = ['rating', 'created_date']

class ReviewEditView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [CheckRolePermission]

    def get_queryset(self):
        return Review.objects.filter(guest=self.request.user)

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class RulesViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = RulesSerializer