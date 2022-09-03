from category.models import Category, Brand
from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.

class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=1000, blank=True)
    price           = models.IntegerField()
    
    images          = models.ImageField(upload_to = 'photos/products')
    image2          = models.ImageField(upload_to = 'photos/products', blank=True)
    image3          = models.ImageField(upload_to = 'photos/products', blank=True)
    image4          = models.ImageField(upload_to = 'photos/products', blank=True)
    
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    brand           = models.ForeignKey(Brand, on_delete= models.CASCADE, null=True)
    category        = models.ForeignKey(Category, on_delete= models.CASCADE, null=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug ])
    
    def __str__(self):
        return self.product_name
    
    
class VariationManager(models.Manager):
    def ram_sizes(self):
        return super(VariationManager ,self).filter(variation_category = 'ram_size', is_active=True)

#     def powers(self):
#         return super(VariationManager ,self).filter(variation_category = 'power' ,is_active=True)


variation_category_choice = (
#   ('power','power'),
    ('ram_size','ram_size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value