from django.contrib import admin
from .models import Category, Brand

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('category_name',)}
    list_display = ('category_name', 'slug')

class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('brand_name',)}
    list_display = ('brand_name', 'slug', 'brand_logo')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)