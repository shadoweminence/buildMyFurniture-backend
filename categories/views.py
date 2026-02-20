from categories.serializer import CategorySerializer
from rest_framework import viewsets
from .models import Category
from rest_framework.parsers import MultiPartParser, FormParser


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parser_classes = (MultiPartParser, FormParser)  # for image upload
