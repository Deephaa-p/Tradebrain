from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import logging
logger = logging.getLogger(__name__)


class RegisterView(APIView):
    permission_classes = [AllowAny]
    """API endpoint for user registration.
    Allows users to register by providing a username, email, and password.
    Returns a success message with user details upon successful registration.
    """
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not password:
            logger.error("Username and password are required.")
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            logger.error("Username already exists.")
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)

        logger.info(f"User registered successfully: {username}")
        return Response({
            'message': 'User registered successfully',
            'data': {
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)

