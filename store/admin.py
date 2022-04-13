from django.contrib import admin
from .models import Product, ReviewRating


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('book_name',)}
    list_display = ('book_name', 'writer', 'genre', 'price',
                    'stock', 'is_available', 'modified_date')


admin.site.register(Product, ProductAdmin)
admin.site.register(ReviewRating)
