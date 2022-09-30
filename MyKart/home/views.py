from django.shortcuts import render
# from django.views.decorators.cache import never_cache
from store.models import Product, ReviewRating


# Create your views here.

# @never_cache
def index(request):
    products = Product.objects.all().filter(is_available=True).order_by('-created_date')
     
    # Get the reviews
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': products,
        'reviews' : reviews
    }
    return render(request, 'index.html', context)