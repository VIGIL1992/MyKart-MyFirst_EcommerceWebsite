from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>',views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id> /<int:cart_item_id>/',views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('update_cart/', views.update_cart, name='update_cart'),
    
    path('checkout/', views.checkout, name='checkout'),
    
    path("apply_coupon", views.Check_coupon, name="apply_coupon"),
]
