from venv import logger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class ResetPasswordView(APIView):
    """
    Allows a user to reset password by providing username and current password,
    without needing authentication or email.
    """
    permission_classes = []
    
    def post(self, request):
        try:
            username = request.data.get("username")
            new_password = request.data.get("new_password")

            if not username or not new_password:
                logger.error("Username and new password are required.")
                return Response(
                    {"error": "username, old_password, and new_password are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                logger.error(f"User with username {username} does not exist.")
                return Response({"error": "Invalid username."}, status=status.HTTP_404_NOT_FOUND)
            
            user.set_password(new_password)
            user.save()
            logger.info(f"Password reset successful for user: {username}")
            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"An error occurred while resetting password: {str(e)}")
            return Response({"error": "An error occurred while resetting password."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
