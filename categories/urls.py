from categories.views import CategoryListCreateAPIView, CategoryDetailAPIView
from django.urls import path

urlpatterns = [
    path("categories/", CategoryListCreateAPIView.as_view()),
    path("categories/<int:pk>", CategoryDetailAPIView.as_view()),
]
