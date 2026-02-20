from categories.serializer import CategorySerializer
from rest_framework import viewsets
from .models import Category


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
