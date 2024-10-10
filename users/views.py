from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import User
from .serializers import UserSignupSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # Automatically raise validation errors
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # Automatically raise validation errors
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Use authenticate to verify credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            # Login successful, return user info or token if applicable
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'Login successful',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
                'email': user.email,
                'phone_number': user.phone_number,
                'is_normal_user': user.is_normal_user,
                'is_restaurant_owner': user.is_restaurant_owner,
            }, status=HTTP_200_OK)

        # Login failed due to invalid credentials
        return Response({'error': 'Invalid credentials'}, status=HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Get the authenticated user
        user_data = {
            'username': user.username,
            'email': user.email,
            'is_normal_user': user.is_normal_user,
            'is_restaurant_owner': user.is_restaurant_owner,
        }
        return Response(user_data)
