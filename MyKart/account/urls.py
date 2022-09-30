from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('', views.user_dashboard, name='user_dashboard'),
    
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    
    path('forgetPassword/', views.forgetPassword, name='forgetPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    
    path('my_orders/', views.my_orders, name='my_orders'),
    path('order_detail/<slug:order_id>', views.order_detail, name='order_detail'),
    path("cancel_order/<slug:pk>/", views.cancel_order, name="cancel_order"),
    
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    
    #address
    path("add_address/", views.add_address, name="add_address"),
    path("edit_address/<int:pk>/", views.edit_address, name="edit_address"),
    path("delete_address/<int:pk>/",views.delete_address,name="delete_address"),
    path("set_default_address/<int:pk>/",views.set_default_address,name="set_default_address"),
    
    #wishlist
    path('add_to_wishlist/<int:id>/',views.add_to_wishlist,name="add_to_wishlist"),
    path('delete_wishlist/<int:id>/',views.delete_wishlist,name="delete_wishlist"),
    path('wishlist/',views.wishlist,name='wishlist'),

]