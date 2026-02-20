from auths.views import RefreshAccessTokenView
from auths.views import ResetPasswordView
from auths.views import ForgotPasswordView
from django.urls import path, include
from .views import RegisterUserView, LoginUserView, ProfileView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginUserView.as_view(), name="login"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("refresh/", RefreshAccessTokenView.as_view(), name="refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path(
        "reset-password/<str:uid>/<str:token>/",
        ResetPasswordView.as_view(),
        name="reset-password",
    ),
]
