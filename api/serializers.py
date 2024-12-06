from rest_framework import serializers
from api.models import User
from .models import UserPreferences


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

     # validating password and confirm password while Registration

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."})
        return attrs
     #    if passwor != password2:
     #        raise serializers.ValidationError(
     #            "password and confirm password doesn't match")
     #    return attrs

    def create(self, validate_data):
        # Remove password2 from the data
        validate_data.pop('password2')
        user = User.objects.create_user(**validate_data)
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ['genres', 'watched_anime']

    def __str__(self):
        return f"Preferences for {self.instance.user.email}" if self.instance else "Preferences Serializer"
