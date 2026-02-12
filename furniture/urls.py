from django.urls import path, include
from .views import UserViewSet, RegisterUserViewSet, LoginUserView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet,basename='user')
router.register(r'register', RegisterUserViewSet,basename='register')

urlpatterns = [
    path('',include(router.urls)),
    path('login/', LoginUserView.as_view(), name='login'),
]