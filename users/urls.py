from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.homepage, name='homepage'),

    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("verify-otp/<str:email>/", views.verify_otp, name="verify_otp"),
    path("reset-password/<str:email>/", views.reset_password, name="reset_password"),
]