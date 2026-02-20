from categories.serializer import CategorySerializer
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import Product
from categories.models import Category
from django.utils.text import slugify


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=100,
        validators=[
            UniqueValidator(
                queryset=Product.objects.all(), message="name should be unique"
            )
        ],
    )
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def validate(self, data):
        # auto generate slug if not provided
        if not data.get("slug"):
            data["slug"] = slugify(data.get("name"))
        return data

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None
