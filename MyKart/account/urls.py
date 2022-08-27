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
]