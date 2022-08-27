from django.urls import path
from . import views

urlpatterns = [
    path('', views.owner, name='owner'),
    path('users/', views.users, name='users'),
    path('adduser/', views.adduser, name='adduser'),
    # path('deleteuser/<user_id>/', views.deleteuser, name='deleteuser'),
    path('blockuser/<user_id>/', views.blockuser, name='blockuser'),
    path('unblockuser/<user_id>/', views.unblockuser, name='unblockuser'),
    
    path('product/', views.product, name='product'),
    # path('addproduct/', views.addproduct, name='addproduct'),
    path('addnewproduct/', views.addnewproduct, name='addnewproduct'),
    path('deleteproduct/<product_id>/', views.deleteproduct, name='deleteproduct'),
    path('product_edit/<product_id>/', views.product_edit, name='product_edit'),
    
    path('category/', views.category, name='category'),
    path('category_add/', views.category_add, name='category_add'),
    path('category_edit/<cat_id>', views.category_edit, name='category_edit'),
    path('category_delete/<category_id>', views.category_delete, name='category_delete'),
    
    path('brand/', views.brand, name='brand'),
    path('brand_add/', views.brand_add, name='brand_add'),
    path('brand_edit/<brand_id>', views.brand_edit, name='brand_edit'),
    path('brand_delete/<brand_id>', views.brand_delete, name='brand_delete'),
       
]
