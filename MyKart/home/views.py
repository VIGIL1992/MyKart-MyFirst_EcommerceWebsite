from django.shortcuts import render
# from django.views.decorators.cache import never_cache
from store.models import Product


# Create your views here.

# @never_cache
def index(request):
     products = Product.objects.all().filter(is_available=True)
     
     context = {
         'products': products,
     }
     return render(request, 'index.html', context)