from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

import requests
from django.conf import settings
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class GoogleLoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'No token provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify token with Google
            response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={token}')
            
            if response.status_code != 200:
                return Response({'error': 'Invalid token', 'details': response.json()}, status=status.HTTP_400_BAD_REQUEST)
            
            user_data = response.json()
            
            # Verify Audience (Optional but recommended)
            # if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            #     return Response({'error': 'Invalid audience'}, status=status.HTTP_400_BAD_REQUEST)

            email = user_data.get('email')
            if not email:
                return Response({'error': 'Email not found in token'}, status=status.HTTP_400_BAD_REQUEST)

            # Get or Create User
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                username = email.split('@')[0]
                # Ensure username is unique
                base_username = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=user_data.get('given_name', ''),
                    last_name=user_data.get('family_name', '')
                )
                user.set_unusable_password()
                user.save()

            # Generate Tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_data': UserSerializer(user).data
            })

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)