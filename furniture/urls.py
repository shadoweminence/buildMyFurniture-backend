from furniture.views import RefreshAccessTokenView
from furniture.views import ResetPasswordView
from furniture.views import ForgotPasswordView
from django.urls import path, include
from .views import UserViewSet, RegisterUserViewSet, LoginUserView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"register", RegisterUserViewSet, basename="register")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginUserView.as_view(), name="login"),
    path("refresh/", RefreshAccessTokenView.as_view(), name="refresh"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path(
        "reset-password/<str:uid>/<str:token>/",
        ResetPasswordView.as_view(),
        name="reset-password",
    ),
]
