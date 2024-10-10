from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number',
                  'is_normal_user', 'is_restaurant_owner']
        extra_kwargs = {
            'password': {'write_only': True},  # Make password write-only
            'is_normal_user': {'required': True},
            'is_restaurant_owner': {'required': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():  # Case insensitive
            raise serializers.ValidationError("Email is already in use.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():  # Case insensitive
            raise serializers.ValidationError("Username is already in use.")
        return value

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return UserSignupSerializer(user).data  # Return serialized user data


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username or password")

        attrs['user'] = user  # Store the authenticated user
        return attrs

    def create_jwt(self, user):
        # Generate JWT tokens (refresh and access)
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'is_normal_user': user.is_normal_user,
            'is_restaurant_owner': user.is_restaurant_owner,
        }
