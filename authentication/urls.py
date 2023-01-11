from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [    
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('activate-account/<str:uid>/<str:token>/', views.Activate_Account.as_view(), name = 'activate account'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name = 'get jwt token')
]
