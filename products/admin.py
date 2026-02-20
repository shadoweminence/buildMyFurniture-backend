from django.contrib import admin
from .models import Product

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "slug",
        "description",
        "price",
        "stock",
        "is_available",
        "created_at",
        "updated_at",
    )
    search_fields = ("name",)
    list_per_page = 25
