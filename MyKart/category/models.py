from django.urls import reverse
from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    cat_image = models.ImageField(upload_to = 'photos/categies', blank=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'catagories'
        
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])
    
    def __str__(self):
        return self.category_name
    
    
class Brand(models.Model):
    brand_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    brand_logo = models.ImageField(upload_to = 'photos/brand', blank=True)
    
    
    
    def __str__(self):
        return self.brand_name