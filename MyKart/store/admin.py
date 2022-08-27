from django.contrib import admin
from .models import Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','product_name', 'brand', 'category', 'price', 'stock',  'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    list_display_links = ('product_name'),

admin.site.register(Product, ProductAdmin)