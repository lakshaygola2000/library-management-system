import logging
import traceback

from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterUserSerializer, LoginUserSerializer, UserSerializer


# Configure logging
logger = logging.getLogger(__name__)


class RegisterUserView(APIView):
    """
    View for registering a new user.
    """
    permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerializer
    
    def post(self, request):
        try:
            # Validate request data
            serializer = self.serializer_class(data=request.data)

            # Create user
            if serializer.is_valid():
                logger.debug("Validated user, creating user...")
                user = serializer.save()

                # Generate JWT tokens
                token = RefreshToken.for_user(user)

                # Return response
                return Response(data={
                    "message": "User registered successfully",
                    "data": {
                        "user": UserSerializer(user).data,
                        "access_token": str(token.access_token),
                        "refresh_token": str(token)
                    }  
                }, status=status.HTTP_201_CREATED)
            
            # Return validation errors
            logger.error(f"Validation errors: {serializer.errors}")
            return Response(data={
                "message": "Validation errors",
                "data": {
                    "errors": serializer.errors
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(f"Internal server error: {e}")
            logger.error(traceback.format_exc())
            return Response(data={
                "message": "Internal server error",
                "data": {
                    "error": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginUserView(APIView):
    """
    View for logging in a user.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginUserSerializer

    def post(self, request):
        try:
            # Validate request data
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            # Authenticate user
            user = authenticate(username=username, password=password)
            
            if not user:
                logger.error(f"Invalid credentials for user: {username}")
                return Response(data={
                    "success": False,
                    "message": "Invalid credentials",
                    "data": {
                        "errors": ["Invalid username or password"]
                    }
                }, status=status.HTTP_401_UNAUTHORIZED)

            # Generate JWT tokens
            token = RefreshToken.for_user(user)

            # Return response
            return Response(data={
                "success": True,
                "message": "User logged in successfully",
                "data": {
                    "user": UserSerializer(user).data,
                    "access_token": str(token.access_token),
                    "refresh_token": str(token)
                }
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Internal server error: {e}")
            logger.error(traceback.format_exc())
            return Response(data={
                "success": False,
                "message": "Internal server error",
                "data": {
                    "error": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutUserView(APIView):
    """
    View for logging out a user.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # Get the user's refresh token
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response(data={
                    "success": False,
                    "message": "Refresh token is required",
                    "data": {
                        "errors": ["Refresh token is required"]
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(data={
                "success": True,
                "message": "User logged out successfully",
                "data": {
                    "message": "User logged out successfully"
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Internal server error: {e}")
            logger.error(traceback.format_exc())
            return Response(data={
                "success": False,
                "message": "Internal server error",
                "data": {
                    "error": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HealthCheckView(APIView):
    """
    View for checking the health of the server.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(data={
            "success": True,
            "message": "Server is running",
            "data": {
                "message": "Server is running"
            }
        }, status=status.HTTP_200_OK)
