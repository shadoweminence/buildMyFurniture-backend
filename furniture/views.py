from django.utils.encoding import force_str
from furniture.serializer import ResetPasswordSerializer
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.views import APIView
from .models import User
from rest_framework import viewsets
from .serializer import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


# from rest_framework.permissions import IsAuthenticated

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginUserView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "message": "User logged in successfully",
            },
            status=status.HTTP_200_OK,
        )


class RefreshAccessTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            old_refresh_token = RefreshToken(refresh_token)
            new_access_token = str(old_refresh_token.access_token)

            if True:
                # blacklist refresh token if BLACKLIST_AFTER_ROTATION=True
                old_refresh_token.blacklist()
                user_id = old_refresh_token.payload.get("user_id")
                user = User.objects.get(id=user_id)

                # Issue a new refresh token for this user
                new_refresh_token = RefreshToken.for_user(
                    user
                )  # issue a new refresh token
                return Response(
                    {"access": new_access_token, "refresh": str(new_refresh_token)},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "access": new_access_token,
                },
                status=status.HTTP_200_OK,
            )
        except TokenError as e:
            return Response(
                {"error": "Invalid or expired refresh token", "details": str(e)},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class RegisterUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": "User created successfully",
            },
            status=status.HTTP_201_CREATED,
        )


class ForgotPasswordView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        reset_link = f"http://localhost:8000/reset-password/{uid}/{token}/"

        send_mail(
            subject="Reset Password",
            message=(
                f"Use the link below to reset your password:\n\n"
                f"{reset_link}\n\n"
                f"UID: {uid}\n"
                f"Token: {token}\n"
            ),
            from_email="[EMAIL_ADDRESS]",
            recipient_list=[user.email],
        )
        return Response(
            {
                "message": "Reset Link sent ",
            },
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    def post(self, request, uid, token):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)

        # Validate token BEFORE doing anything else
        is_valid = PasswordResetTokenGenerator().check_token(user, token)

        if not is_valid:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_password = serializer.validated_data["new_password"]
        user.set_password(new_password)
        user.save()
        return Response(
            {"message": "Password changed successfully"},
            status=status.HTTP_200_OK,
        )
