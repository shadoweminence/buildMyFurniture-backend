from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import Category
from django.utils.text import slugify


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=100, validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        model = Category
        fields = "__all__"

    def validate(self, data):
        # auto generate slug if not provided
        if not data.get("slug"):
            data["slug"] = slugify(data.get("name"))
        return data
