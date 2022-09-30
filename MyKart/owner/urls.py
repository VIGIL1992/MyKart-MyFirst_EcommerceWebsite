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
     path("addproductgallery", views.addproductgallery, name="addproductgallery"),
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
    
    path('activeorders/', views.activeorders, name='activeorders'),
    path("order_history", views.order_history, name="order_history"),
    path("admin_order_detail/<order_id>/", views.admin_order_detail, name="admin_order_detail"),
    path("order_status_change/",views.order_status_change,name="order_status_change"), 
    path("product_report", views.product_report, name="product_report"),
    path("sales_report", views.sales_report, name="sales_report"),
    
    path("product_export_csv",views.product_export_csv,name="product_export_csv"),
    path("product_export_pdf",views.product_export_pdf,name="product_export_pdf"),
    path("sales_export_csv", views.sales_export_csv, name="sales_export_csv"),
    path("sales_export_pdf", views.sales_export_pdf, name="sales_export_pdf"),
    
]
