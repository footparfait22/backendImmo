from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='profile.role', read_only=True)
    avatar = serializers.ImageField(source='profile.avatar', required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'avatar', 'is_staff', 'is_superuser']

    def update(self, instance, validated_data):
        # source='profile.avatar' maps 'avatar' in input to 'instance.profile.avatar'
        # DRF's ModelSerializer might have trouble with writable nested dots if profile isn't clearly writable.
        profile_data = validated_data.pop('profile', None)
        if profile_data and 'avatar' in profile_data:
            instance.profile.avatar = profile_data['avatar']
            instance.profile.save()
            
        return super().update(instance, validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, default='client')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role', 'client')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        # Profile is created by signal, just update role
        user.profile.role = role
        user.profile.save()
        return user

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.profile.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_data'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'role': self.user.profile.role if hasattr(self.user, 'profile') else 'client'
        }
        return data