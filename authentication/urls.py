from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('activate-account/<str:uid>/<str:token>/',
         views.Activate_Account.as_view(), name='activate account'),
    path('request-password-reset/', views.Request_Password_Reset.as_view(),
         name='request password reset'),
    path('reset-password/<str:uid>/<str:token>/',
         views.Reset_Password.as_view(), name='reset password'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='get jwt token'),
    path('api/token/verify/', views.verify_token, name='verify token'),
]
